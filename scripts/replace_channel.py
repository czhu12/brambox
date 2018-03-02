#!/usr/bin/env python
import argparse
import cv2

import brambox as bb


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='This script replaces a channel from input 1 with a channel from input 2 and saves the output as a new image')
    parser.add_argument('inputimage', nargs=2, help='Filename of the 2 images')
    parser.add_argument('--output', '-o', help='Output filename', default='out.jpg')
    parser.add_argument('--channels', '-c', metavar='N', nargs=2, help='Zero-based index of the channel to replace (old new)', default=['0', '0'])
    args = parser.parse_args()

    # Parse input
    img = [cv2.imread(f) for f in args.inputimage]
    number_of_channels = img[0].shape[2] if len(img[0].shape) >= 3 else 1
    channels = [(0, i) for i in range(number_of_channels)]
    channels[int(args.channels[0])] = (1, int(args.channels[1]))

    # Mix channels
    mixer = bb.transforms.ChannelMixer(number_of_channels)
    mixer.set_channels(channels)
    out = mixer(*img)

    # Save output
    cv2.imwrite(args.output, out)


if __name__ == '__main__':
    main()
