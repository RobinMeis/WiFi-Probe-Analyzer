import xmltodict
from manuf import manuf

class network:
    def __init__(self, manuf, BSSID, ESSID, RSSI, channel, location): #Create a new network
        self.BSSID = BSSID
        self.ESSID = ESSID
        self.RSSI = RSSI
        self.channel = channel
        self.location = location
        self.manuf = manuf
        self.manufacturer = self.manuf.get_manuf(BSSID)
        self.devices = []

    def addClient(self, MAC): #Add a device to network
        if (MAC != self.BSSID and MAC not in self.devices): #Add only if devices MAC is not equal to BSSID
            self.devices.append(MAC)
            return True
        else:
            return False

class parser:
    def __init__(self, xml):
        self.netxml = xmltodict.parse(xml)
        self.networks = {}
        self.manuf = manuf.MacParser(update=True)

    def getLocation(self, network): #Gets the best available location information
        try: #Check if location is available
            location = network["gps-info"]
        except KeyError: #Return none if GPS was unavailable
            return None
        else: #Find best location information
            coordinates = {}
            if (float(location["peak-lat"]) != 0.0 or float(location["peak-lon"]) != 0.0): #Use peak information if available
                coordinates["latitude"] = float(location["peak-lat"])
                coordinates["longitude"] = float(location["peak-lon"])
            else: #Otherwise use average
                coordinates["latitude"] = float(location["avg-lat"])
                coordinates["longitude"] = float(location["avg-lon"])

            return coordinates

    def handleInfrastructure(self, net, location): #Parses an infrastructure network
        BSSID = net["BSSID"] #Get basic information
        RSSI = int(net["snr-info"]["max_signal_dbm"])
        channel = net["channel"]
        try: #Chek wether the network sends an ESSID
            ESSID = net["SSID"]["essid"]["#text"]
        except KeyError:
            ESSID = None

        if (BSSID in self.networks): #Check if network is already known
            if (self.networks[BSSID].RSSI < RSSI): #In case of better RSSI...
                self.networks[BSSID].RSSI = RSSI
                self.networks[BSSID].location = location #...update location
        else: #If not, add new network
            self.networks[BSSID] = network(self.manuf, BSSID, ESSID, RSSI, channel, location)

        clients = net["wireless-client"] #Add clients to network
        for client in clients:
            try:
                if (client["client-mac"] != BSSID):
                    self.networks[BSSID].addClient(client["client-mac"])
            except TypeError:
                pass

    def parse(self):
        networks = self.netxml["detection-run"]["wireless-network"]
        for network in networks: #Decide how to handle a network
            location = self.getLocation(network)
            if (location != None):
                if (network["@type"] == "infrastructure"): #Handle infrastructure networks
                    self.handleInfrastructure(network, location)
                elif (network["@type"] == "probe"): #We could do something with this as well!
                    pass

    def getNetworks(self):
        return self.networks
