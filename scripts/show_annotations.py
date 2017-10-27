#!python

import os
import argparse
import brambox as bb


def main():

    parser = argparse.ArgumentParser(description='Render text annotations on images')
    parser.add_argument('format', choices=bb.annotations.formats.keys(), help='Annotation format')
    parser.add_argument('annofile', help='Annotation file or annotation file sequence, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('imagefolder', help='Image folder')
    parser.add_argument('--show-labels', action='store_true', help='Show labels next to bounding boxes')
    parser.add_argument('--stride', type=int, default=1, help='Only show every N\'th image')
    parser.add_argument('--offset', type=int, default=0, help='Start with an offset, may be negative')
    parser.add_argument('--fps', dest='fps', type=int, default=0, help='Frames per second to show, if 0, use space bar to go to next frame')
    parser.add_argument('--image-width', type=int, default=None, help='Image width info for relative annotation formats')
    parser.add_argument('--image-height', type=int, default=None, help='Image height info for relative annotation formats')
    parser.add_argument('--class-names', default=None, help="Class label file for annotation formats using indexes rather than class names")

    args = parser.parse_args()

    class_names = None
    if args.class_names is not None:
        class_names = []
        with open(args.class_names) as f:
            class_names = f.read().splitlines()

    annotations = bb.annotations.parse(args.format, args.annofile,
                        image_width=args.image_width,
                        image_height=args.image_height,
                        class_label_map=args.class_names,
                        stride=args.stride, offset=args.offset)

    bb.annotations.show_annotations(annotations, args.imagefolder, show_labels=args.show_labels)

if __name__ == '__main__':
    main()
