#!python

import os
import cv2
import math
import time
import argparse
import threading

from brambox.annotations import formats

colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 0),
    (255, 255, 255),
    (0, 0, 0)
]


def parse_files(annofile, anno_fmt, video_file):

    print("Parsing annotations...")
    annotations = []
    if '%' in annofile:
        # its a series of annotation files
        counter = 0
        while True:
            filename = annofile % counter
            counter += 1

            if not os.path.exists(filename):
                break

            with open(filename, "r") as f:
                lines = f.readlines()

            imgannos = []
            for line in lines:
                imgannos.append(formats[anno_fmt](line))

            annotations.append(imgannos)

    else:
        raise NotImplementedError

    cap = cv2.VideoCapture(video_file)
    number_of_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    images = []
    frame_counter = 0

    while True:
        ret, image = cap.read()
        if not ret:
            break
        images.append(image)
        frame_counter += 1
        print("Reading video frames", int(100 * frame_counter / number_of_frames), "%", end='\r')
    print("")

    assert len(images) == len(annotations)

    return annotations, images


def show(annos, images, stride, fps):

    cv2.namedWindow("Annotations", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Annotations", 640, 480)

    print("Rendering boxes...")
    for i in range(0, len(annos), stride):

        # multiple annotations per image
        for j, anno in enumerate(annos[i]):
            pt1 = (int(anno.x_top_left), int(anno.y_top_left))
            pt2 = (int(anno.x_top_left + anno.width), int(anno.y_top_left + anno.height))
            if anno.occluded:
                thickness = 2
            else:
                thickness = 5

            cv2.rectangle(images[i], pt1, pt2, colors[j % len(colors)], thickness)

        text = "{}/{}".format(i, len(images))
        height, width, _ = images[i].shape
        cv2.putText(images[i], text, (10, int(height) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    print("Showtime!")
    prev = time.time()
    for image in images:
        start = time.time()
        cv2.imshow("Annotations", image)
        diff = (time.time() - start) * 1000
        if fps == 0:
            cv2.waitKey(0)
        elif cv2.waitKey(int(1000.0/fps - diff)) == ord(' '):
            cv2.waitKey(0)

    print("Done")


def main():

    parser = argparse.ArgumentParser(description='Render text annotations on images')
    parser.add_argument('format', choices=formats.keys(), help='Annotation format')
    parser.add_argument('annofile', help='Annotation file or annotation file sequence, for example: path/to/anno/I%%08d.txt')
    parser.add_argument('videofile', help='Videofile or image sequence, for example: path/to/images/I%%08d.png')
    parser.add_argument('--stride', dest='stride', type=int, default=1, help='Only show every N\'th image')
    parser.add_argument('--fps', dest='fps', type=int, default=0, help='Frames per second to show, if 0, use space bar to go to next frame')

    args = parser.parse_args()

    annos, images = parse_files(args.annofile, args.format, args.videofile)
    show(annos, images, args.stride, args.fps)


if __name__ == '__main__':
    main()
