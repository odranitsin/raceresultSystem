__author__ = 'james'

import csv
import random
from datetime import *
from time import sleep
import requests
import grequests
import threading

class Simulator(threading.Thread):
    ##INITALISE VARIABLES
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Simulator,self).__init__(group=group, target=target, name=name, verbose=verbose)
        self.args = args;
        self.kwargs = kwargs;
        self.passingsBuffer  = "";
        self.passingCount    = 0
        self.location        = {'longitude': round(8.423955 + (random.random()-0.5)/100.0, 6), 'latitude': round(49.011791 + (random.random()-0.5)/100.0, 6)}
        self.timeDilation    = 1;
        self.density         = 30;
        self.firstPassing    = datetime.now();
        self.raceTimeStart   = datetime.now();
        self.bibRange        = range(1, 20000 + 1);
        self.device          = 'SIM-' + '{:03d}'.format(random.randint(0,999));
        self.user            = '';
        self.pw              = '';
        self.key             = '';
        self.uploadWaitTime  = 0.2;
        
        self._isRunning      = True;
        self._sendPassings   = False;
        self._sendStatus     = True;

        self.simulationStartDate    = self.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.simulationStart        = self.now()
        self.nextStatus             = self.now()
        self.nextPassing            = self.racetime()
        self.uploadLastPassingTime  = self.now()

        self.fileNum         = 0;

    def getSimulationSlot(self):
        resp = str(requests.get("https://data.raceresult.com/interface/passings/simulations/getSimulationSlot.php?user=" + str(self.user) + "&pw=" + str(self.pw)).text);
        if ";" in resp:
            self.fileNum         = int(resp.split(";")[1]);
            self.device          = resp.split(";")[0];
            self.key             = resp.split(";")[2];
            print "$$ NEW DEVICE " + self.device + " WITH FILE NUMBER " + str(self.fileNum) + " $$\r\n",
        else:
            self._isRunning = False
            print "FAILED\r\n",

    def now(self):
        return datetime.now()
        
    def randomBib(self):
        return self.bibRange.pop( random.randint(1, len(self.bibRange)) - 1);
        
    def racetime(self):
        return self.raceTimeStart + self.timeDilation*(self.now()-self.simulationStart)

    def writeStatus(self):
        url = "https://data.raceresult.com/interface/passings/simulations/sendStatus.php?user=" + str(self.user) \
                + "&device=" + self.device \
                + "&file=" + str(self.fileNum) \
                + "&key=" + self.key \
                + "&time=" + self.racetime().strftime("%H:%M:%S.%f")[:12] \
                + "&count=" + str(self.passingCount) \
                + "&loc=" + str(self.location['latitude'] + (random.random()-0.5)/1000.0 ) + ";" + str(self.location['longitude'] + (random.random()-0.5)/1000.0);
        r = grequests.get(url);
        r.send();
        self.nextStatus += timedelta(minutes=1);
        if self._sendPassings: print str(self.device) + ": STATUS SENT\tnext:" + str(self.nextStatus) + "\r\n",

    def writePassing(self, num):
        print str(self.device) + ": PASSING #" + str(num) + "\r\n",
        url = "https://data.raceresult.com/interface/passings/simulations/sendPassing.php?user=" + str(self.user) \
                + "&device=" + str(self.device) \
                + "&file=" + str(self.fileNum) \
                + "&key=" + self.key \
                + "&date=" + self.nextPassing.strftime("%Y-%m-%d") \
                + "&time=" + '{:.3f}'.format((self.nextPassing - self.simulationStartDate).total_seconds()) \
                + "&bib=" + str(self.randomBib()) \
                + "&num=" + str(num);
        r = grequests.get(url);
        r.send();
        self.uploadLastPassingTime = self.now();
        td = random.expovariate(self.density / 60.0);
        self.nextPassing += timedelta(seconds=td);

    def stop(self):
        self._isRunning = False;

    def beginSimulation(self):
        self.firstPassing    = self.now();
        self.nextPassing     = self.racetime();
        self._sendPassings = True;
        self._sendStatus = True;

    def run(self):
        self.writeStatus();
        while self._isRunning:
            if (len(self.bibRange) == 0):
                print str(self.device) + ": No more bibs available" + "\r\n",
                break;

            if self._sendPassings:
                if self.nextPassing < self.racetime():
                    self.passingCount += 1;
                    self.writePassing(self.passingCount);
                
            if self._sendStatus:    
                if self.nextStatus < self.now():
                    self.writeStatus();

            if not (self._sendPassings and self._sendStatus):
                sleepTime = 0.5;
            elif (self.nextPassing < self.nextStatus):
                sleepTime = (self.nextPassing - self.racetime()).total_seconds()
            else:
                sleepTime = (self.nextStatus - self.now()).total_seconds()

            ##print "WAIT TIME: " + str(sleepTime);
            sleep(min(max(sleepTime, 0), 0.5)); ## sleep for 'sleepTime' with min=0 and max=0.5
