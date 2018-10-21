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
        cur.execute("SELECT `ESSID`, `channel`, `RSSImax`, `latitude`, `longitude`, `manufacturer` FROM `networks` WHERE `BSSID` = %s LIMIT 1", (BSSID,))
        row = cur.fetchone()
        if (row != None):
            location = {"latitude": row["latitude"], "longitude": row["longitude"]}
            return network(BSSID, row["ESSID"], row["RSSImax"], row["channel"], location, row["manufacturer"])
        else:
            return None

    def updateNetwork(self, network):
        cur = self.cnx.cursor()
        values = (network.ESSID, network.channel, network.RSSI, network.location["latitude"], network.location["longitude"], network.manufacturer, network.BSSID)
        cur.execute("UPDATE `networks` SET `ESSID` = %s, `channel` = %s, `RSSImax` = %s, `latitude` = %s, `longitude` = %s, `manufacturer` = %s WHERE `BSSID` = %s", values)
        self.cnx.commit()
