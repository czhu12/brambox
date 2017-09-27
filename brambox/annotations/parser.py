#
#   Copyright EAVISE
#

import os
from .formats import formats

__all__ = ["parse"]


def parse(filename, fmt, frame_width, frame_height):
    """ parse a set of annotations given a specific format to a generic representation

    The function will return a list of lists, where every inner list contains a number
    of Annotation objects. The inner lists represent the annotations per image. The outer
    list represents the annotations for all images
    filename    -- single filename or sequence expression (containing %d)
    fmt         -- annotation format (string)
    frame_width -- needed for relative annotation formats
    frame_height -- needed for relative annotation formats
    """

    annotations = []
    if '%' in filename:
        # its a series of annotation files
        frame_counter = 0
        while True:
            fn = filename % frame_counter

            if not os.path.exists(fn):
                break

            with open(fn, "r") as f:
                lines = f.readlines()

            annos_per_image = []
            for line in lines:
                annos_per_image.append(formats[fmt](line, frame_number=frame_counter,
                                                frame_width=frame_width,
                                                frame_height=frame_height))
            annotations.append(annos_per_image)
            frame_counter += 1

    else:
        # its a single annotation file for one or more images
        annotations_flat = []
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            # assume these formats include a frame number field
            annotations_flat.append(formats[fmt](line, frame_width=frame_width,
                                            frame_height=frame_height))

        # group annotations per image
        annotations_flat = sorted(annotations_flat, key=lambda annotation: annotation.frame_number)
        next_frame_number = annotations[0].frame_number
        annos_per_image = []
        for annotation in annotations_flat:

            if annotation.frame_number != next_frame_number:
                annotations.append(annos_per_image)
                next_frame_number = annotation.frame_number
                annos_per_image = []

            annos_per_image.append(annotation)


    return annotations

