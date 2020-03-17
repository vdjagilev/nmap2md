#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser
import columns_definition

__version__ = "1.0.0"

supported_columns = [
    'port',
    'state',
    'service',
    'version'
]

parser = OptionParser(usage="%prog [options] file.xml", version="%prog " + __version__)

# Different variations of columns:
# port: port number
# state: port state (open, closed)
# protocol: protocol where port is located
# service: service name (http, ssh)
# product: application name
# version: application version
parser.add_option("-c", "--columns", default="Port,State,Service,Version", help="define a columns for the table")
parser.add_option("--hs", default=0, type="int", help="address is used as a header, this option defines header number h1 -> h6")
parser.add_option("-r", "--rows", default="define rows which will report certain data")

(options, args) = parser.parse_args()

columns = list(column for column in options.columns.split(",") if column in supported_columns)
result = {}
md = ""

# Wrong header number, downgrading to default value: 1
if options.hs < 0 or options.hs > 6:
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

        state = port.find("state")
        service_node = port.find("service")

        if service_node is None:
            service = False
        else:
            service = service_node.attrib

        port_info.append({
            "port": port.attrib.get("portid", "") + "/" + port.attrib.get("protocol", ""),
            "state": state.get("state", ""),
            "service": service.get("name", "") if service else '',
            "version": service.get("product", "") + " " + service.get("version", "") if service else '',
        })

    result[address] = port_info

# Start converting data to Markdown
# Herenow IP addresses are defined as a header
for address in result:
    if options.hs != 0:
        md += "%s %s\n\n" % ('#' * options.hs, address)
    md += "| %s |" % " | ".join(columns)
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
