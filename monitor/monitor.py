from scapy.all import *
from probes import *
from db import *
import time
import re
from manuf import manuf

class monitor:
    def __init__(self, configuration):
        self.configuration = configuration
        self.db = mysql_connector(configuration["mysql_host"], configuration["mysql_user"], configuration["mysql_password"], configuration["mysql_db"])
        self.db.connect()
        self.probes = probes(configuration["session_timeout"])
        self.probes.threadStart()
        self.probes.setCallback(DEVICE_NEW, self.deviceNew)
        self.probes.setCallback(DEVICE_TIMEOUT, self.deviceTimeout)
        sniff (iface=configuration["interface"], prn=self.PacketHandler, store=0)
        self.manuf = manuf.MacParser(update=True)

    def PacketHandler(self, pkt):
        if pkt.type == 0 and pkt.subtype == 0x04: #If packet is probe
            manufacturer = self.manuf.get_manuf(pkt.addr2)
            try:
                self.probes.probe(pkt.addr2, pkt.info.decode('UTF-8'), manufacturer, self.configuration["latitude"], self.configuration["longitude"])
            except UnicodeDecodeError: #Ignore ESSID in case of encoding proble$
                self.probes.probe(pkt.addr2, None, manufacturer, self.configuration["latitude"], self.configuration["longitude"])


        else: #otherwise just check if device probed earlier and update last seen
            self.probes.seen(pkt.addr2)

    def deviceNew(self, device):
        print("%s [%s] New device" % (time.strftime("%Y-%m-%d %H:%M:%S"), device.MAC,))

    def deviceTimeout(self, device):
        print("%s [%s] Timeout" % (time.strftime("%Y-%m-%d %H:%M:%S"), device.MAC,))
        self.db.storeDevice(device)

configuration = {}
with open("config.txt") as config:
    for line in config:
        line = re.match("(.*):\"(.*)\".*", line)
        if (line != None):
            configuration[line.group(1)] = line.group(2)

configuration["session_timeout"] = int(configuration["session_timeout"])

monitoring = monitor(configuration)
