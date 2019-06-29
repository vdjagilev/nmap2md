#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser

__version__ = "1.0.0"

supported_columns = [
    'port',
    'protocol',
    'service',
    'product',
    'version'
]

parser = OptionParser(usage="%prog [options] file.xml", version="%prog " + __version__)

# Different variations of columns:
# port: port number
# protocol: protocol where port is located
# service: service name (http, ssh)
# product: application name
# version: application version
parser.add_option("-c", "--columns", default="port,service,product", help="choice of the columns for the table. Example: %s" % ",".join(supported_columns))
parser.add_option("--hs", default=1, type="int", help="address is used as a header, this option defines header number h1 -> h6")

(options, args) = parser.parse_args()

columns = list(column for column in options.columns.split(",") if column in supported_columns)
result = {}
md = ""

# Wrong header number, downgrading to default value: 1
if options.hs < 1 or options.hs > 6:
    options.hs = 1

try:
    tree = ET.parse(args[0])
except IndexError:
    print("[Err] No file could be found")
    print()
    parser.print_help()
    sys.exit()

for host in tree.getroot().findall("host"):
    address = host.find("address").attrib["addr"]
    port_info = []
    for port in host.find("ports").findall("port"):
        service = port.find("service").attrib
        port_info.append({
            "port": port.attrib.get("portid", ""),
            "protocol": port.attrib.get("protocol", ""),
            "service": service.get("name", ""),
            "product": service.get("product", ""),
            "version": service.get("version", "")
        })
    
    result[address] = port_info

# Start converting data to Markdown
# Herenow IP addresses are defined as a header
for address in result:
    md += "%s %s\n\n" % ('#' * options.hs, address)
    md += "| %s |" % " | ".join(map(lambda s: s.title(), columns))
    md += "\n"
    
    # Adding +2 for 1 space on left and right sides
    md += "|%s|" % "|".join(map(lambda s: '-' * (len(s) + 2), columns))
    md += "\n"

    for port_info in result[address]:
        # Calculating correct amount of spaces to add some padding and justify content in the cell
        # Currently it does not work if content is bigger than the column, in any case it does not break the Markdown view
        md += "| %s |" % " | ".join(map(lambda s: port_info[s] + (' ' * (len(s) - len(port_info[s]))), columns))
        md += "\n"
    
    md += "\n\n"


print(md)
