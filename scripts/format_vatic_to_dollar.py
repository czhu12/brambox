#!python

import os
import argparse

from brambox.annotations import VaticAnnotation
from brambox.annotations import DollarAnnotation


def main():

    parser = argparse.ArgumentParser(description='Convert a vatic annotation format text file to a set of dollar annotation text files')
    parser.add_argument('inputfile', help='Input VATIC file')
    parser.add_argument('outputfolder', help='output folder to store dollar files, note that the folder must exist')

    args = parser.parse_args()

    with open(args.inputfile) as f:
        lines = f.readlines()

    # convert lines to a list of VaticAnnotation objects
    vatic_annotations = []
    for line in lines:
        vatic_annotations += [VaticAnnotation(line)]

    # sort by framenumber
    vatic_annotations = sorted(vatic_annotations, key=lambda annotation: annotation.frame_number)

    next_frame_number = 0
    text = []
    for vatic_annotation in vatic_annotations:

        if vatic_annotation.frame_number != next_frame_number:
            filename = os.path.join(args.outputfolder, "I{:08d}.txt".format(next_frame_number))
            with open(filename, 'w') as f:
                f.write("\n".join(text))

            next_frame_number = vatic_annotation.frame_number
            text = []

        text += [DollarAnnotation(vatic_annotation).serialize()]

if __name__ == '__main__':
    main()
