import mysql.connector

class mysql_connector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None
        self.storage_queue = []

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def disconnect(self):
        if (self.cnx != None):
            self.cnx.close()

    def reconnect(self):
        try:
            self.cnx.reconnect(attempts=1, delay=0)
        except mysql.connector.errors.InterfaceError:
            return False
        else:
            return True

    def addDevice(self, MAC, firstSeen, lastSeen): #Add new device to database
        cursor = self.cnx.cursor() #Check for existing device
        checkDevice = "SELECT `MAC` FROM `devices` WHERE `MAC` = %s LIMIT 1"
        dataDevice = (MAC)
        cursor.execute(checkDevice, dataDevice)

        if (cursor.rowcount() == 0): #Add if not in DB yet
            cursor = self.cnx.cursor()
            addDevice = "INSERT INTO `devices` (`MAC`, `firstSeen`, `lastSeen`) VALUES (%s, %s, %s)"
            dataDevice = (MAC, firstSeen, lastSeen)
            cursor.execute(addDevice, dataDevice)
            return True
        else:
            return False

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

    def addSession(self, MAC, firstSeen, lastSeen, seenCount, latitude, longitude): #Add new Session to database
        cursor = self.cnx.cursor()
        addSession = "INSERT INTO `sessions` (`deviceID`, `firstSeen`, `lastSeen`, `seenCount`, `latitude`, `longitude`) VALUES ((SELECT `id` FROM `devices` WHERE `mac` = %s), %s, %s, %s, %s, %s)"
        dataSession = (MAC, firstSeen, lastSeen, seenCount, latitude, longitude)
        cursor.execute(addSession, dataSession)
        return cursor.lastrowid

    def addESSIDrelation(self, sessionID, ESSID): #Creates a relation between a session and an ESSID
        cursor = self.cnx.cursor()
        addRelation = "INSERT INTO `sessionESSIDs` (`sessionID`, `ESSIDid`) VALUES (%s, (SELECT `id` FROM `ESSIDs` WHERE `ESSID` = %s))"
        dataRelation = (sessionID, ESSID)
        cursor.execute(addRelation, dataRelation)

    def storeDevice(self, device):
        self.storage_queue.append(device) #Put into storage queue. In case of connection issues, this will avoid data loss
        self.toDB() #Write to database

    def toDB(self):
        for i in range(0, len(self.storage_queue)): #Try to write data to database
            device = self.storage_queue.pop()
            try:
                self.handleDevice(device.MAC, device.firstSeen, device.lastSeen)
                sessionID = self.addSession(device.MAC, device.firstSeen, device.lastSeen, device.seenCount, device.latitude, device.longitude)

                for ESSID in device.ESSIDs:
                    self.handleESSID(ESSID, device.firstSeen, device.lastSeen)
                    self.addESSIDrelation(sessionID, ESSID)

                self.cnx.commit()
            except mysql.connector.errors.OperationalError:
                self.storage_queue.append(device)
                if not self.reconnect(): #If reconnect failed, retry after next timeout
                    break
