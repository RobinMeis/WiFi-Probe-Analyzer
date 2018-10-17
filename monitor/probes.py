import datetime
import time
import threading

DEVICE_NEW = 0
DEVICE_TIMEOUT = 1

class device:
    def __init__(self, MAC): #Creates a new device instance
        self.MAC = MAC
        self.firstSeen = datetime.datetime.now()
        self.lastSeen = self.firstSeen
        self.seenCount = 1
        self.ESSIDs = set()
        self.threadRun = False
        self.threadID = None

    def seen(self): #Called if device is seen again
        self.lastSeen = datetime.datetime.now()
        self.seenCount += 1

    def addESSID(self, ESSID): #Adds an ESSID...
        if (ESSID != "" and ESSID != None): #...if an ESSID has been sent by the device
            self.ESSIDs.add(ESSID)

class probes:
    def __init__(self, timeout=500):
        self.devices = {}
        self.newCallback = None
        self.timeoutCallback = None
        self.timeout = timeout

    def seen(self, deviceMAC): #A device was seen, but not as a probe request. This might happen if a device is associated to an AP after sendg a probe request
        try:
            self.devices[deviceMAC].seen() #Check if device known and update last seen
        except KeyError: #Do nothing if device is unknown
            pass

    def probe(self, deviceMAC, ESSID): #A probe request (from scapy)
        try:
            self.devices[deviceMAC].seen() #Check if device known and update last seen
        except KeyError:
            self.devices[deviceMAC] = device(deviceMAC) #Create new device
            if (self.newCallback != None): #If available, call calback
                self.newCallback(self.devices[deviceMAC])

        self.devices[deviceMAC].addESSID(ESSID) #Store probed ESSID (if available)

    def checkExpired(self): #Checks for devices which reached timeout (has to be called regularly)
        devices = self.devices.copy()
        for deviceMAC in devices:
            device = self.devices[deviceMAC]
            if (device.lastSeen < datetime.datetime.now() - datetime.timedelta(seconds=self.timeout)): #Timeout reached?
                del self.devices[deviceMAC] #Unregister device
                if (self.timeoutCallback != None): #If available, call calback
                    self.timeoutCallback(device)

    def setCallback(self, type, callback): #Sets a callback. Set to None to disable a callback
        if (type == DEVICE_NEW):
            self.newCallback = callback
        elif (type == DEVICE_TIMEOUT):
            self.timeoutCallback = callback

    def _thread(self): #Thread for calling checkExpired periodically
        while (self.threadRun):
            self.checkExpired()
            time.sleep(5)

    def threadStart(self): #Starts thread
        self.threadRun = True
        self.threadID = threading.Thread(target=self._thread)
        self.threadID.start()

    def threadStop(self): #Stops thread
        self.threadRun = False
        self.threadID.join()
