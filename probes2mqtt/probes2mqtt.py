from scapy.all import *

clientprobes = set()
def PacketHandler(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        if len(pkt.info) > 0:
            print(pkt.addr2 + " -> " + pkt.addr1 + " : " + pkt.info.decode("UTF-8"))

sniff (iface="alfamon", prn=PacketHandler)
