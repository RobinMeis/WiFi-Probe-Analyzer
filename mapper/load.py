import netxml

with open("mapper.netxml") as xml: #Load networks and parse
    parser = netxml.parser(xml.read())
    parser.parse()

print(parser.getNetworks())
