#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#

import os
import cv2

from ..annotations import annotation as anno
from ..detections import detection as det

__all__ = ['draw_box', 'show_bounding_boxes']


def draw_box(img, boxes, color=None, show_labels=False, inline=False):
    """ Returns an image with the bounding boxes drawn

        img         : image to draw on
        boxes       : list of bounding boxes to draw
        color       : color to use for drawing (if none, every label will get its own color, up to 8 labels)
        show_labels : whether or not to print the label names
        inline      : whether to draw on the image or take a copy
    """
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

    if inline:
        output = img
    else:
        output = img.copy()

    label_color = {}
    color_counter = 0
    for box in boxes:
        thickness = 4
        text = box.class_label

        # Type specific settings
        if isinstance(box, anno.Annotation):
            if box.lost:
                continue
            if box.occluded:
                thickness = 2
        elif isinstance(box, det.Detection):
            text = '{} {:.2f}%'.format(box.class_label, box.confidence)

        # get coord
        pt1 = (int(box.x_top_left), int(anno.y_top_left))
        pt2 = (int(box.x_top_left + anno.width), int(anno.y_top_left + anno.height))

        # get color
        if color is not None:
            use_color = color
        else:
            if box.class_label in label_color:
                use_color = label_color[box.class_label]
            else:
                use_color = colors[color_counter]
                label_color[box.class_label] = use_color
                color_counter = (color_counter + 1) % len(colors)

        # draw rect
        cv2.rectangle(output, pt1, pt2, use_color, 2)

        # write label
        if show_labels:
            cv2.putText(output, text, (pt1[0], pt1[1]-5), cv2.FONT_HERSHEY_PLAIN, 0.75, use_color, 1, cv2.LINE_AA)


def show_bounding_boxes(boxes, img_folder, img_ext='.png', show_labels=False, color=None, get_img_fn=None):
    """ Display the bounding boxes parsed by the generic parse function

        boxes       : Dictionary containing bounding boxes (eg. output of parse())
        img_folder  : Folder containing the images
        img_ext     : Extension of the images
        show_labels : Boolean indicating whether or not to display the labels on the images
        get_img_fn  : Function that will be called to get the image path. Gets called with : img_id, img_folder, img_ext
    """
    print('Showing bounding boxes:\n\tPress a key to show the next image\n\tPress ESC to stop viewing images')

    if get_img_fn is None:
        get_img_fn = lambda img_id, img_folder, img_ext: os.path.join(img_folder, img_id+img_ext)

    if color is None:
        text_col = (0, 0, 255)
    else:
        text_col = color

    for img_id, box in sorted(boxes.items()):
        img_path = get_img_fn(img_id, img_folder, img_ext)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        draw_box(img, box, color, show_labels, True)
        if show_labels:
            cv2.putText(img, img_id, (10, 15), cv2.FONT_HERSHEY_PLAIN, 0.75, text_col, 1, cv2.LINE_AA)

        cv2.imshow('Image annotations', img)
        while True:
            keycode = cv2.waitKey(0)
            if keycode == 27:
                return
            elif keycode == ord('m'):
                print(img_id)
            else:
                break
