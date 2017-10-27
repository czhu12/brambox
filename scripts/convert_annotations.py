#!python

import os
import sys
import argparse

from brambox.annotations import formats
from brambox.annotations.util.convert import parse, generate


def main():

    parser = argparse.ArgumentParser(description='Convert annotation file(s) from one format to the other')
    parser.add_argument('inputformat', choices=formats.keys(), help='Input annotation format')
    parser.add_argument('inputannotations', help='Input annotation file or sequence expression, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('outputformat', choices=formats.keys(), help='Ouput annotation format')
    parser.add_argument('outputannotations', help='Output annotation file or folder')
    parser.add_argument('--image-width', dest='image_width', type=int, default=None, help='Image width info for relative annotation formats')
    parser.add_argument('--image-height', dest='image_height', type=int, default=None, help='Image height info for relative annotation formats')
    parser.add_argument('--class-names', dest='class_names', default=None, help="Class label file for annotation formats using indexes rather than class names")
    parser.add_argument('--stride', type=int, default=1, help='If a sequence expression is given as input, this stride is used')
    parser.add_argument('--offset', type=int, default=0, help='If a sequence expression is given as input, this offset is used')

    args = parser.parse_args()

    indir = os.path.split(args.inputannotations)[0]
    if not os.path.exists(indir):
        sys.exit("Input directory {} does not exist".format(indir))

    if os.path.splitext(args.outputannotations)[1] != '':
        outdir = os.path.split(args.outputannotations)[0]
    else:
        outdir = args.outputannotations

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    class_names = None
    if args.class_names is not None:
        class_names = []
        with open(args.class_names) as f:
            class_names = f.read().splitlines()

    annotations = parse(args.inputformat, args.inputannotations,
                        image_width=args.image_width,
                        image_height=args.image_height,
                        class_label_map=class_names,
                        stride=args.stride,
                        offset=args.offset)

    generate(args.outputformat, annotations, args.outputannotations,
             image_width=args.image_width,
             image_height=args.image_height,
             class_label_map=class_names)

    print("Converted", len(annotations), "files")

if __name__ == '__main__':
    main()
