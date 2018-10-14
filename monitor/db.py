import datetime
import mysql.connector

class mysql_connector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def disconnect(self):
        if (self.cnx != None):
            self.cnx.close()

    def addDevice(self, MAC, firstSeen, lastSeen): #Add new device to database
        try: #Try to add device to database
            cursor = self.cnx.cursor()
            addDevice = "INSERT INTO `devices` (`MAC`, `firstSeen`, `lastSeen`) VALUES (%s, %s, %s)"
            dataDevice = (MAC, firstSeen, lastSeen)
            cursor.execute(addDevice, dataDevice)
        except mysql.connector.errors.IntegrityError: #If device does exist...
            return False #...return false...
        else:
            return True #...otherwise true

    def seenDevice(self, MAC, lastSeen): #Update last seen timestamp of a device
        cursor = self.cnx.cursor()
        seenDevice = "UPDATE `devices` SET `lastSeen` = %s WHERE `MAC` = %s"
        dataDevice = (lastSeen, MAC)
        cursor.execute(seenDevice, dataDevice)

    def handleDevice(self, MAC, firstSeen, lastSeen): #Handle a seen device
        if (not self.addDevice(MAC, firstSeen, lastSeen)): #Try to add device, if fails...
            self.seenDevice(MAC, lastSeen) #...just update last seen timestamp

    def addESSID(self, ESSID, firstSeen, lastSeen): #Add new ESSID to database
        try: #Try to add ESSID to database
            cursor = self.cnx.cursor()
            addESSID = "INSERT INTO `ESSIDs` (`ESSID`, `firstSeen`, `lastSeen`) VALUES (%s, %s, %s)"
            dataESSID = (ESSID, firstSeen, lastSeen)
            cursor.execute(addESSID, dataESSID)
        except mysql.connector.errors.IntegrityError: #If ESSID does exist...
            return False #...return false...
        else:
            return True #...otherwise true

    def seenESSID(self, ESSID, lastSeen): #Update last seen timestamp of a device
        cursor = self.cnx.cursor()
        seenESSID = "UPDATE `ESSIDs` SET `lastSeen` = %s WHERE `ESSID` = %s"
        dataESSID = (lastSeen, ESSID)
        cursor.execute(seenESSID, dataESSID)

    def handleESSID(self, ESSID, firstSeen, lastSeen): #Handle a seen ESSID
        if (not self.addESSID(ESSID, firstSeen, lastSeen)): #Try to add ESSID, if fails...
            self.seenESSID(ESSID, lastSeen) #...just update last seen timestamp

    def addSession(self, MAC, firstSeen, lastSeen, seenCount, location): #Add new Session to database
        cursor = self.cnx.cursor()
        addSession = "INSERT INTO `sessions` (`deviceID`, `firstSeen`, `lastSeen`, `seenCount`, `location`) VALUES ((SELECT `id` FROM `devices` WHERE `mac` = %s), %s, %s, %s, %s)"
        dataSession = (MAC, firstSeen, lastSeen, seenCount, location)
        cursor.execute(addSession, dataSession)
        return cursor.lastrowid

    def addESSIDrelation(self, sessionID, ESSID): #Creates a relation between a session and an ESSID
        cursor = self.cnx.cursor()
        addRelation = "INSERT INTO `sessionESSIDs` (`sessionID`, `ESSIDid`) VALUES (%s, (SELECT `id` FROM `ESSIDs` WHERE `ESSID` = %s))"
        dataRelation = (sessionID, ESSID)
        cursor.execute(addRelation, dataRelation)

    def storeDevice(self, location, device):
        self.handleDevice(device.MAC, device.firstSeen, device.lastSeen)
        sessionID = self.addSession(device.MAC, device.firstSeen, device.lastSeen, device.seenCount, location)

        for ESSID in device.ESSIDs:
            self.handleESSID(ESSID, device.firstSeen, device.lastSeen)
            self.addESSIDrelation(sessionID, ESSID)

        self.cnx.commit()
