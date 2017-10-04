#!/usr/bin/env python
#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import argparse
import cv2

from brambox.transforms import ChannelMixer


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='This script swaps a channel from input1 with a channel from input2 and saves the output')
    parser.add_argument('inputimage', nargs=2, help='Filename of the 2 images')
    parser.add_argument('-o', '--output', help='Output filename', default='out.jpg')
    parser.add_argument('-c', '--channels', nargs=2, help='Channel to swap (old new)', default=['0', '0'])
    args = parser.parse_args()

    # Parse input
    img = [cv2.imread(f) for f in args.inputimage]
    number_of_channels = img[0].shape[2] if len(img[0].shape) >= 3 else 1
    channels = [(0, i) for i in range(number_of_channels)]
    channels[int(args.channels[0])] = (1, int(args.channels[1]))

    # Mix channels
    mix = ChannelMixer(number_of_channels)
    mix.setChannels(channels)
    mix.setInputImages(*img)
    out = mix.getOutputImage()

    # Save output
    cv2.imwrite(args.output, out)

if __name__ == '__main__':
    main()
