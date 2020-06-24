#!/usr/bin/env python
import sys
from translate.storage import po

FNV1_32_INIT = 0x811c9dc5
FNV_32_PRIME = 0x01000193

def fnv1a_32(data, hval=FNV1_32_INIT):
    for byte in data:
        hval ^= byte
        hval = (hval * FNV_32_PRIME) & 0xffffffff
    return hval

def po2ymo(infile, outfile, includefuzzy=False, encoding='utf-16le'):
    inputstore = po.pofile(infile)

    units = {}
    for unit in inputstore.units:
        if unit.istranslated() or (unit.isfuzzy() and includefuzzy and unit.target):
            source = unit.source
            context = unit.getcontext()
            if context:
                source = context + '\004' + source
            hash = fnv1a_32(source.encode(encoding))
            units[hash] = unit.target.encode(encoding) + bytes(2)

    byteorder='little'
    outfile.write(len(units).to_bytes(2, byteorder)) # len

    offset = 2 + len(units) * (4 + 2)
    for hash, data in units.items():
        outfile.write(hash.to_bytes(4, byteorder))
        outfile.write(offset.to_bytes(2, byteorder))
        offset += len(data)

    for data in units.values():
        outfile.write(data)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("uasge: po2ymo.py <infile> <outfile>")
        sys.exit()
    infile = open(sys.argv[1], 'rb')
    outfile = open(sys.argv[2], 'wb')
    po2ymo(infile, outfile)
