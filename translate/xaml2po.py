#!/usr/bin/env python
from translate.convert import convert
from translate.storage import po
from xml.dom.minidom import parse, Node

def xaml2po(node, store):
    for n in node.childNodes:
        if n.nodeType == Node.ELEMENT_NODE:
            if (n.hasAttribute('Text')):
                unit = po.pounit(n.getAttribute('Text'))
                unit.addlocation(f'{n.nodeName}:{n.getAttribute("Name")}')
                store.addunit(unit)
            xaml2po(n, store)

def run_converter(inputfile, outputfile, templatefile=None):
    xml = parse(inputfile)
    target_store = po.pofile()
    xaml2po(xml, target_store)
    target_store.serialize(outputfile)
    return 1

def main(argv=None):
    formats = {'xaml': ('po', run_converter)}
    parser = convert.ConvertOptionParser(formats, description=__doc__)
    parser.run(argv)

if __name__ == '__main__':
    main()
