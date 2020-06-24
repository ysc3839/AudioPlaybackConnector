#!/usr/bin/env python
import sys
from xml.dom.minidom import parse, Node

def xamlmin(node):
    for n in node.childNodes:
        if n.nodeType == Node.TEXT_NODE and n.nodeValue:
            n.nodeValue = n.nodeValue.strip()
        elif n.nodeType == Node.ELEMENT_NODE:
            xamlmin(n)

def run_converter(infile, outfile):
    xml = parse(infile)
    xamlmin(xml)
    xml.normalize()

    xml_str = xml.toxml()
    i = xml_str.find('?>') # remove prefix '<?xml version="1.0" ?>'
    xml_str = xml_str[i+2:]

    outfile.write(xml_str.encode('utf-16le'))
    outfile.write(bytes(2)) # null terminator

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("uasge: xamlmin.py <infile> <outfile>")
        sys.exit()
    infile = open(sys.argv[1], 'rb')
    outfile = open(sys.argv[2], 'wb')
    run_converter(infile, outfile)
