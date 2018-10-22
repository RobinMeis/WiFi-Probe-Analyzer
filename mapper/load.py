import netxml
import db
import re

configuration = {} #Load configuration
with open("config.txt") as config:
    for line in config:
        line = re.match("(.*):\"(.*)\".*", line)
        if (line != None):
            configuration[line.group(1)] = line.group(2)

with open("mapper.netxml") as xml: #Load networks and parse
    parser = netxml.parser(xml.read())
    parser.parse()

db = db.mysql_connector(configuration["mysql_host"], configuration["mysql_user"], configuration["mysql_password"], configuration["mysql_db"])
db.connect()
networks = parser.getNetworks()
for BSSID in networks:
    xmlNetwork = networks[BSSID]
    dbNetwork = db.getNetwork(BSSID)
    print("%s (%s) 📶%d" % (xmlNetwork.ESSID, xmlNetwork.BSSID, xmlNetwork.RSSI))
    if (dbNetwork == None): #If network does not exist yet...
        dbNetwork = db.addNetwork(xmlNetwork) #...add it
    elif (dbNetwork.RSSI < xmlNetwork.RSSI): #if networks exists and RSSI of xmlNetwork is higher...
        db.updateNetwork(xmlNetwork) #...update network

    for MAC in xmlNetwork.devices:
        device = xmlNetwork.devices[MAC]
        print("   %s" % (device.MAC))
        deviceID = db.getDeviceID(device)
        if (deviceID == None):
            deviceID = db.addDevice(device).ID
        else:
            db.updateDevice(device)
        relationID = db.getRelationID(deviceID, dbNetwork.ID)
        if (relationID == None):
            db.addRelation(deviceID, dbNetwork.ID)
db.disconnect()
