#!/usr/bin/env python
from translate.convert import convert
from translate.storage import po
from xml.dom.minidom import parse, Node

def po2xaml(node, names):
    for n in node.childNodes:
        if n.nodeType == Node.TEXT_NODE and n.nodeValue:
            n.nodeValue = n.nodeValue.strip()
        elif n.nodeType == Node.ELEMENT_NODE:
            if (n.hasAttribute('Text')):
                n.setAttribute('Text', names[n.getAttribute('Name')])
            po2xaml(n, names)

def run_converter(inputfile, outputfile, templatefile, includefuzzy=False):
    source_store = po.pofile(inputfile)
    names = {}
    for unit in source_store.units:
        if unit.istranslated() or (unit.isfuzzy() and includefuzzy and unit.target):
            loc, = unit.getlocations()
            tag_name, name = loc.split(':')
            names[name] = unit.target

    xml = parse(templatefile)
    po2xaml(xml, names)
    xml.normalize()

    xml_str = xml.toxml()
    i = xml_str.find('?>') # remove prefix '<?xml version="1.0" ?>'
    xml_str = xml_str[i+2:]

    outputfile.write(xml_str.encode('utf-16le'))
    outputfile.write(bytes(2)) # null terminator
    return 1

def main(argv=None):
    formats = {('po', 'xaml'): ('xaml', run_converter)}
    parser = convert.ConvertOptionParser(formats, usetemplates=True, description=__doc__)
    parser.run(argv)

if __name__ == '__main__':
    main()
