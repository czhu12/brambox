#!/usr/bin/env python
#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import os
import argparse
import xml.etree.ElementTree as ET

from brambox.annotations import PascalVOCAnnotation
from brambox.annotations import DarknetAnnotation


def convert(infile, outfile, names):
    pascal = PascalVOCAnnotation(None, names)
    darknet = []
    root = ET.parse(infile).getroot()
    img_width = int(root.find('size').find('width').text)
    img_height = int(root.find('size').find('height').text)
    obj = root.findall('object')

    for o in obj:
        darknet += [DarknetAnnotation(img_width, img_height, pascal.deserialize(o)).serialize()]

    with open(outfile, 'w') as f:
        f.write("\n".join(darknet))


def main():
    parser = argparse.ArgumentParser(description='Convert Pascal VOC annotation file(s) to darknet')
    parser.add_argument('input', help='input file or folder')
    parser.add_argument('output', help='output file or folder')
    parser.add_argument('-n', '--names', help='names file for darknet')
    args = parser.parse_args()

    # Parse names file
    if args.names is not None:
        with open(args.names, 'r') as f:
            names = f.read().splitlines()
    else:
        names = None

    # Convert format
    assert os.path.exists(args.input), 'Invalid input'

    if os.path.isdir(args.input):
        assert os.path.isdir(args.output), 'Output and input should both be folders'

        for filename in os.listdir(args.input):
            if not filename.endswith('.xml'):
                continue

            infile = os.path.join(args.input, filename)
            outfile = os.path.join(args.output, filename.rsplit('.', 1)[0] + '.txt')
            convert(infile, outfile, names)

    else:
        assert not os.path.isdir(args.output), 'Output and input should both be files'
        convert(args.input, args.output, names)

if __name__ == '__main__':
    main()
