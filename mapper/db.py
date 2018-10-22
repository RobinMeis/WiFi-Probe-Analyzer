import mysql.connector

class network:
    def __init__(self, BSSID, ESSID, RSSI, channel, location, manufacturer): #Create a new network
        self.BSSID = BSSID
        self.ESSID = ESSID
        self.RSSI = RSSI
        self.channel = channel
        self.location = location
        self.manufacturer = manufacturer
        self.devices = []

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

    def addNetwork(self, network):
        cur = self.cnx.cursor()
        values = (network.BSSID, network.ESSID, network.channel, network.RSSI, network.location["latitude"], network.location["longitude"], network.manufacturer)
        cur.execute("INSERT INTO `networks` (`BSSID`, `ESSID`, `channel`, `RSSImax`, `latitude`, `longitude`, `manufacturer`) VALUES (%s, %s, %s, %s, %s, %s, %s)", values)
        self.cnx.commit()

    def getNetwork(self, BSSID):
        cur = self.cnx.cursor(dictionary=True)
        cur.execute("SELECT `id`, `ESSID`, `channel`, `RSSImax`, `latitude`, `longitude`, `manufacturer` FROM `networks` WHERE `BSSID` = %s LIMIT 1", (BSSID,))
        row = cur.fetchone()
        if (row != None):
            location = {"latitude": row["latitude"], "longitude": row["longitude"]}
            net = network(BSSID, row["ESSID"], row["RSSImax"], row["channel"], location, row["manufacturer"])
            net.ID = row["id"]
            return net
        else:
            return None

    def updateNetwork(self, network):
        cur = self.cnx.cursor()
        values = (network.ESSID, network.channel, network.RSSI, network.location["latitude"], network.location["longitude"], network.manufacturer, network.BSSID)
        cur.execute("UPDATE `networks` SET `ESSID` = %s, `channel` = %s, `RSSImax` = %s, `latitude` = %s, `longitude` = %s, `manufacturer` = %s WHERE `BSSID` = %s", values)
        self.cnx.commit()

    def getDeviceID(self, device):
        cur = self.cnx.cursor(dictionary=True)
        cur.execute("SELECT `id` FROM `devices` WHERE `MAC` = %s LIMIT 1", (device.MAC,))
        row = cur.fetchone()
        if (row != None):
            return row["id"]
        else:
            return None

    def addDevice(self, device):
        cur = self.cnx.cursor()
        values = (device.MAC, device.manufacturer)
        cur.execute("INSERT INTO `devices` (`MAC`, `firstSeen`, `lastSeen`, `sessionCount`, `probesSeen`, `connectedSeen`, `manufacturer`) VALUES (%s, UTC_TIMESTAMP(), UTC_TIMESTAMP(), 0, 0, 1, %s)", values)
        self.cnx.commit()
        device.ID = cursor.lastrowid
        return device

    def updateDevice(self, device):
        cur = self.cnx.cursor()
        values = (device.MAC,)
        cur.execute("UPDATE `devices` SET `lastSeen` = UTC_TIMESTAMP(), `connectedSeen` = 1 WHERE `MAC` = %s", values)
        self.cnx.commit()

    def getRelationID(self, deviceID, networkID):
        cur = self.cnx.cursor()
        cur.execute("SELECT `id` FROM `connectedDevices` WHERE `deviceID` = %s and `networkID` = %s", (deviceID, networkID))
        row = cur.fetchone()
        if (row != None):
            return row["id"]
        else:
            return None

    def addRelation(self, deviceID, networkID):
        cur = self.cnx.cursor()
        values = (deviceID, networkID)
        cur.execute("INSERT INTO `connectedDevices` (`deviceID`, `networkID`) VALUES (%s, %s)", values)
        self.cnx.commit()
