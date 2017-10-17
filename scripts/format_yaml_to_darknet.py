#!/usr/bin/env python
#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import os
import argparse

from brambox.annotations import DarknetParser, YamlParser


def main():
    parser = argparse.ArgumentParser(description='Convert from yaml to darknet')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output folder')
    parser.add_argument('-n', '--names', help='names file for darknet')
    parser.add_argument('-d', '--dimension', help='Image dimension for darknet', nargs=2, type=int)
    args = parser.parse_args()

    # Read input
    with open(args.input, 'r') as f:
        lines = f.read()

    if args.names is not None:
        with open(args.names, 'r') as f:
            names = f.read().splitlines()
    else:
        names = None

    # Create parsers
    in_parser = YamlParser()
    out_parser = DarknetParser(image_width=args.dimension[0], image_height=args.dimension[1], class_label_map=names)

    # Convert (in this case: Single file -> Multi file)
    annotations = in_parser.deserialize(lines)
    for img_id in annotations:
        res_string = out_parser.serialize(annotations[img_id])
        with open(os.path.join(args.output, img_id+'.txt'), 'w') as f:
            f.write(res_string)


if __name__ == '__main__':
    main()
