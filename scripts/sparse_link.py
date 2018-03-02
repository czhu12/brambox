#!/usr/bin/env python
import os
import sys
import argparse

import brambox.boxes as bbb


def create_link(src, dst, hard, override):
    if override and os.path.exists(dst):
        os.remove(dst)

    if hard:
        os.link(src, dst)
    else:
        os.symlink(src, dst)


def main():
    parser = argparse.ArgumentParser(description='Create a directory with symbolic links to files in another directory')
    parser.add_argument('inputdir', help='Input directory')
    parser.add_argument('outputdir', help='Output directory')
    parser.add_argument('--stride', '-s', metavar='N', type=int, default=1, help="Only create a symlink for every n'th file where n is this parameter")
    parser.add_argument('--offset', '-o', metavar='N', type=int, default=0, help='Start with a certain offset')
    parser.add_argument('--hardlink', '-l', action='store_true', help="Create hardlinks instead of softlinks")
    parser.add_argument('--force', '-f', action='store_true', help="Force override if link already exists")

    args = parser.parse_args()

    filenames = sorted(os.listdir(args.inputdir))

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    for src in bbb.expand(args.inputdir, args.stride, args.offset):
        dst = os.path.join(args.outputdir, os.path.split(src)[1])
        create_link(src, dst, args.hard, args.force)


if __name__ == '__main__':
    main()
