from scapy.all import *
from probes import *
from db import *
import time
import re

class monitor:
    def __init__(self, configuration):
        self.configuration = configuration
        self.db = mysql_connector(configuration["mysql_host"], configuration["mysql_user"], configuration["mysql_password"], configuration["mysql_db"])
        self.db.connect()
        self.probes = probes(configuration["session_timeout"])
        self.probes.threadStart()
        self.probes.setCallback(DEVICE_NEW, self.deviceNew)
        self.probes.setCallback(DEVICE_TIMEOUT, self.deviceTimeout)
        sniff (iface=configuration["interface"], prn=self.PacketHandler)

    def PacketHandler(self, pkt):
        if pkt.type == 0 and pkt.subtype == 0x04:
            self.probes.probe(pkt.addr2, pkt.info.decode('UTF-8'))

    def deviceNew(self, device):
        print("[%s] New device" % (device.MAC,))

    def deviceTimeout(self, device):
        print("[%s] Timeout" % (device.MAC,))
        self.db.storeDevice(self.configuration["location"], device)

configuration = {}
with open("config.txt") as config:
    for line in config:
        line = re.match("(.*):\"(.*)\".*", line)
        configuration[line[1]] = line[2]

configuration["session_timeout"] = int(configuration["session_timeout"])
try:
    configuration["location"]
except KeyError:
    configuration["location"] = None

monitoring = monitor(configuration)
