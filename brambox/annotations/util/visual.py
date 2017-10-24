#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#

import os
import cv2

__all__ = ['draw_anno_img', 'show_annotations']


def draw_anno_img(img, annotations, color=None, show_labels=False, inline=False):
    """ Returns an image with the annotation bounding boxes drawn

        img         : image to draw on
        annotations : list of annotations to draw
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
    for anno in annotations:
        # get coord
        pt1 = (int(anno.x_top_left), int(anno.y_top_left))
        pt2 = (int(anno.x_top_left + anno.width), int(anno.y_top_left + anno.height))

        # get color
        if color is not None:
            use_color = color
        else:
            if anno.class_label in label_color:
                use_color = label_color[anno.class_label]
            else:
                use_color = colors[color_counter]
                label_color[anno.class_label] = use_color
                color_counter = (color_counter + 1) % len(colors)

        # get thickness
        if anno.occluded:
            thickness = 4
        else:
            thickness = 2

        # draw rect
        cv2.rectangle(output, pt1, pt2, use_color, thickness)

        # write label
        if show_labels:
            cv2.putText(output, anno.class_label, (pt1[0], pt1[1]-5), cv2.FONT_HERSHEY_PLAIN, 0.75, use_color, 1, cv2.LINE_AA)


def show_annotations(annotations, img_folder, img_ext='.png', show_labels=False, color=None, get_img_fn=None):
    """ Display the annotations parsed by the generic parse function
        
        annotations : Ditctionary containing annotations (eg. output of parse())
        img_folder  : Folder containing the images
        img_ext     : Extension of the images
        show_labels : Boolean indicating whether or not to display the labels on the images
        get_img_fn  : Function that will be called to get the image path. Gets called with : img_id, img_folder, img_ext
    """
    print('Show annotations function:\n\tPress a key to show the next image\n\tPress ESC to stop viewing annotations')

    if get_img_fn is None:
        get_img_fn = default_get_img

    if color is None:
        text_col = (0,0,255)
    else:
        text_col = color

    for img_id, anno in sorted(annotations.items()):
        img_path = get_img_fn(img_id, img_folder, img_ext)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        draw_anno_img(img, anno, color, show_labels, True)
        if show_labels:
                cv2.putText(img, img_id, (10,15), cv2.FONT_HERSHEY_PLAIN, 0.75, text_col, 1, cv2.LINE_AA)

        cv2.imshow('Image annotations', img)
        keycode = cv2.waitKey(0)
        if keycode == 27:
            return


def default_get_img(img_id, img_folder, img_ext):
    """ Get image path string """
    return os.path.join(img_folder, img_id+img_ext)
