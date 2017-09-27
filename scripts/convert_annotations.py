#!python

import os
import argparse

from brambox.annotations import formats
from brambox.annotations import parse
from brambox.annotations import generate

def main():

    parser = argparse.ArgumentParser(description='Convert a vatic annotation format text file to a set of dollar annotation text files')
    parser.add_argument('inputformat', choices=formats.keys(), help='Input annotation format')
    parser.add_argument('inputannotations', help='Input annotation file or sequence expression, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('outputformat', choices=formats.keys(), help='Ouput annotation format')
    parser.add_argument('outputannotations', help='Output annotation file or sequence expression, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('--image-width', dest='image_width', type=int, default=0, help='Image width info for relative annotation formats')
    parser.add_argument('--image-height', dest='image_height', type=int, default=0, help='Image height info for relative annotation formats')

    args = parser.parse_args()

    # todo check if dirs exist
    annotations = parse(args.inputannotations, args.inputformat, args.image_width, args.image_height)
    generate(annotations, args.outputformat, args.image_width, args.image_height, args.outputannotations)

if __name__ == '__main__':
    main()
