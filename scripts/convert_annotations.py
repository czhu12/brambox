#!python

import os
import sys
import argparse
import brambox.boxes as bbb


class StoreKwargs(argparse.Action):
    """ Store keyword arguments in a dict.
        This action must be used with multiple arguments.
        It will parse ints and floats and leave the rest as strings.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        d = {}
        for items in values:
            n, v = items.split('=')

            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass

            d[n] = v

        setattr(namespace, self.dest, d)


def main():
    parser = argparse.ArgumentParser(
        description='Convert annotation file(s) from one format to the other',
        usage='%(prog)s inputformat inputannotations outputformat outputannotations [optional arguments]',
        epilog=f'Posible formats are: {list(bbb.annotation_formats.keys())}',
    )

    parser.add_argument('inputformat', metavar='inputformat', choices=bbb.annotation_formats.keys(), help='Input annotation format')
    parser.add_argument('inputannotations', help='Input annotation file or sequence expression, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('outputformat', metavar='outputformat', choices=bbb.annotation_formats.keys(), help='Ouput annotation format')
    parser.add_argument('outputannotations', help='Output annotation file or folder')
    parser.add_argument('--stride', type=int, default=1, help='If a sequence expression is given as input, this stride is used')
    parser.add_argument('--offset', type=int, default=0, help='If a sequence expression is given as input, this offset is used')
    parser.add_argument('--kwargs', metavar='KW=V', help='Keyword arguments for the parser', nargs='*', action=StoreKwargs, default={})
    args = parser.parse_args()

    # Parse arguments
    indir = os.path.split(args.inputannotations)[0]
    if not os.path.exists(indir):
        sys.exit(f'Input directory {indir} does not exist')

    if os.path.splitext(args.outputannotations)[1] != '':
        outdir = os.path.split(args.outputannotations)[0]
    else:
        outdir = args.outputannotations

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Convert
    annotations = bbb.parse('anno_'+args.inputformat, args.inputannotations, stride=args.stride, offset=args.offset, **args.kwargs)
    bbb.generate('anno_'+args.outputformat, annotations, args.outputannotations, **args.kwargs)
    print("Converted", len(annotations), "files")


if __name__ == '__main__':
    main()
