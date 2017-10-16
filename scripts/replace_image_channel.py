#!python
#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import argparse
import cv2

from brambox.transforms import ChannelMixer


def replace(colorimage, grayimage, channel, convertcode):
    """ replace procedure with optional color conversion up front.

    Returns the resulting image
    """

    if convertcode >= 0:
        colorimage = cv2.cvtColor(colorimage, convertcode)

    number_of_channels = colorimage.shape[2]
    channels = [(0, i) for i in range(number_of_channels)]
    channels[channel] = (1, 0)

    mixer = ChannelMixer(number_of_channels)
    mixer.set_channels(channels)
    mixer.set_input_images(colorimage, grayimage)
    out = mixer.get_output_image()

    return out


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='This script replaces a color image channel from a multichannel image (RGB, RGBA,...) with a grayscale image channel')
    parser.add_argument('colorimage', help='Color image file or image sequence (for example: I%%08d.png)')
    parser.add_argument('grayimage', help='Grayscale image file or image sequence (for example: I%%08d.png)')
    parser.add_argument('output', help='Output filename or image sequence (for example: I%%08d.png)')
    parser.add_argument('--colorconvert', type=int, default=-1, help='Apply a color conversion on colorimage before replacement. ' + \
                        'By default no conversion is applied. See opencv cv::ColorConversionCodes enum for the integer value to use')
    parser.add_argument('-c', '--channel', type=int, default=0, help='Channel number to be replaced')
    args = parser.parse_args()

    if '%' in args.colorimage and '%' in args.grayimage and '%' in args.output:
        # work with image sequence
        capgray = cv2.VideoCapture(args.grayimage)
        capcolor = cv2.VideoCapture(args.colorimage)
        size = (int(capcolor.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capcolor.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        writer = cv2.VideoWriter(args.output, 0, 0, size)

        while True:
            ret, grayimage = capgray.read()
            if not ret:
                break
            ret, colorimage = capcolor.read()
            if not ret:
                break

            out = replace(colorimage, grayimage, args.channel, args.colorconvert)
            writer.write(out)
    else:
        # process single image
        colorimage = cv2.imread(args.colorimage)
        grayimage = cv2.imread(args.grayimage)

        out = replace(colorimage, grayimage, args.channel, args.colorconvert)
        cv2.imwrite(args.output, out)


if __name__ == '__main__':
    main()
