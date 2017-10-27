#!python
#
#   Yaml to Darknet annotation converter
#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import os
import argparse

import brambox as bb


def main():
    parser = argparse.ArgumentParser(description='Convert from yaml to darknet')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output folder')
    parser.add_argument('-n', '--names', help='names file for darknet')
    parser.add_argument('-d', '--dimension', help='Image dimension for darknet', nargs=2, type=int)
    args = parser.parse_args()

    # Read input
    if args.names is not None:
        with open(args.names, 'r') as f:
            names = f.read().splitlines()
    else:
        names = None

    # Convert annotations
    annotations = bb.annotations.parse('yaml', args.input)
    bb.annotations.generate('darknet', annotations, args.output,
             image_width=args.dimension[0], image_height=args.dimension[1], class_label_map=names)


if __name__ == '__main__':
    main()
