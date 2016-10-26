import RROnline
import getpass

print "#############################################"
print "race|result Online Passings Simulator"
print "#############################################"
print "CTRL + C to quit"
print ""

acc         = int(raw_input("Account Number:\t\t\t"));
pw          = getpass.getpass();
num         = int(raw_input("Number of Devices (max 10):\t"));
density     = int(raw_input("Passings per minute:\t\t"));
bibRange    = int(raw_input("Number of participants:\t\t"));

print ""
print "#############################################"
print ""

def Device():
    p = RROnline.Simulator();
    p.user      = str(acc);
    p.pw        = pw;
    p.bibRange  = range(1, bibRange + 1);
    p.density   = density;
    return p;
    
try:
    deviceList = [];
    for i in xrange(num):
        d = Device();
        d.getSimulationSlot();
        d.start();				##begin thread. Required for multiple devices		
        deviceList.append(d);

    print ""
    print "#############################################"
    print ""
    some_var = raw_input("Press ENTER to start");
    print ""
    print "#############################################"

    for device in deviceList: device.beginSimulation();

    while True:
        #do nothing
        _i = 0;
except:
    #suppress error
    _i = 1;
finally:
    for device in deviceList: device.stop();
    print "#############################################"
    print "Closing..."
