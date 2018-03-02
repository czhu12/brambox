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
        description='Convert bounding box file(s) from one format to the other',
        usage='%(prog)s inputformat inputpath outputformat outputpath [optional arguments]',
        epilog=f'Posible formats are: {list(bbb.formats.keys())}',
    )

    parser.add_argument('inputformat', metavar='inputformat', choices=bbb.formats.keys(), help='Input format')
    parser.add_argument('inputpath', help='Bounding box file, folder or file sequence')
    parser.add_argument('outputformat', metavar='outputformat', choices=bbb.formats.keys(), help='Ouput format')
    parser.add_argument('outputpath', help='Output file or folder')
    parser.add_argument('--stride', '-s', metavar='N', type=int, default=1, help='If a sequence expression is given as input, this stride is used')
    parser.add_argument('--offset', '-o', metavar='N', type=int, default=0, help='If a sequence expression is given as input, this offset is used')
    parser.add_argument('--kwargs', '-k', metavar='KW=V', help='Keyword arguments for the parser', nargs='*', action=StoreKwargs, default={})
    args = parser.parse_args()

    # Parse arguments
    indir = os.path.split(args.inputpath)[0]
    if not os.path.exists(indir):
        sys.exit(f'Input directory {indir} does not exist')

    if os.path.splitext(args.outputpath)[1] != '':
        outdir = os.path.split(args.outputpath)[0]
    else:
        outdir = args.outputpath

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Convert
    bbox = bbb.parse(args.inputformat, args.inputpath, stride=args.stride, offset=args.offset, **args.kwargs)
    bbb.generate(args.outputformat, bbox, args.outputpath, **args.kwargs)
    print(f'Converted {len(bbox)} files')


if __name__ == '__main__':
    main()
