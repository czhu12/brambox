#!python
#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import argparse
import cv2
import os

import brambox as bb


def replace(colorimage, grayimage, channel, convertcode):
    """ replace procedure with optional color conversion up front.

    Returns the resulting image
    """

    if convertcode >= 0:
        colorimage = cv2.cvtColor(colorimage, convertcode)

    number_of_channels = colorimage.shape[2]
    channels = [(0, i) for i in range(number_of_channels)]
    channels[channel] = (1, 0)

    mixer = bb.transforms.ChannelMixer(number_of_channels)
    mixer.set_channels(channels)
    out = mixer(colorimage, grayimage)

    return out


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='This script replaces a color image channel from a multichannel image (RGB, RGBA,...) with a grayscale image channel')
    parser.add_argument('colorimages', help='Color image file(s) selection sequence')
    parser.add_argument('grayimagedir', help='Directory with grayscale images')
    parser.add_argument('outdir', help='Output filename or directory')
    parser.add_argument('--colorconvert', type=int, default=-1, help='Apply a color conversion on colorimage before replacement. ' +
                        'By default no conversion is applied. See opencv cv::ColorConversionCodes enum for the integer value to use')
    parser.add_argument('-c', '--channel', type=int, default=0, help='Channel number to be replaced')
    parser.add_argument('--stride', type=int, default=1, help="For image sequences: only process every n'th file where n is this parameter")
    parser.add_argument('--offset', type=int, default=0, help='For image sequences: start with a certain offset, may be negative')
    args = parser.parse_args()

    for colorfile in bb.annotations.expand(args.colorimages, args.stride, args.offset):
        colorimage = cv2.imread(colorfile)
        commonfilename = os.path.split(colorfile)[1]
        grayimage = cv2.imread(os.path.join(args.grayimagedir, commonfilename))
        if colorimage is None or grayimage is None:
            break
        out = replace(colorimage, grayimage, args.channel, args.colorconvert)
        cv2.imwrite(os.path.join(args.outdir, commonfilename), out)


if __name__ == '__main__':
    main()
