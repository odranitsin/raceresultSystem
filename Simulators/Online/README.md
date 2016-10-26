This folder contains a simulator for generating passings for online device. These resources are targeted to developers wishing to test their implimentation of the race|result System Online Passings API.

Contents
--------------
RROnlineSimulator.exe - executable capable of running up to 10 simulated race|result Systems uploading passings online
/nsrc                  - folder containing the Python source code of the executable RROnlineSimulator.exe

Notes
--------------
- This simulator will only generate passings and status for a simulated device. The simulator cannot respond to commands sent via the sendCommand.php API call.
- The simulator generates passings with random interarrival times, using a expontential distribution.
- Details of the Online Passing API can be found here: https://www.raceresult.com/fw/support/documents/online-storage-api.pdf
