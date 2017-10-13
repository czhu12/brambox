#
#   Copyright EAVISE
#

import os
from .formats import formats

__all__ = ["parse"]


def parse(filename, fmt, **kwargs):
    """ parse a set of annotations given a specific format to a generic representation

    The function will return a list of lists, where every inner list contains a number
    of Annotation objects. The inner lists represent the annotations per image. The outer
    list represents the annotations for all images
    filename    -- single filename or sequence expression (containing %d)
    fmt         -- annotation format (string)
    kwargs      -- additional arguments that are forwarded to the specific annotation format class constructors
    """

    annotations = []

    if os.path.isdir(filename):
        list(os.path.listdir(filename))
        raise NotImplementedError

    elif os.path.isfile(filename):
        # its a single annotation file for one or more images
        annotations_flat = []
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            # NOTE: assume these formats include a frame number field
            # TODO: add error if format does not include frame number field
            try:
                annotations_flat.append(formats[fmt](line, **kwargs))
            except ValueError:
                # line is not deserializable, treat as comment: ignore
                pass

        # group annotations per image
        annotations_flat = sorted(annotations_flat, key=lambda annotation: annotation.frame_number)
        next_frame_number = annotations_flat[0].frame_number
        annos_per_image = []
        for annotation in annotations_flat:

            if annotation.frame_number != next_frame_number:
                annotations.append({'frame_number':annotation.frame_number, 'annotations':annos_per_image})
                next_frame_number = annotation.frame_number
                annos_per_image = []

            annos_per_image.append(annotation)

    elif '%' in filename:
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
                try:
                    annos_per_image.append(formats[fmt](line, **kwargs))
                except ValueError:
                    # line is not deserializable, treat as comment: ignore
                    pass

            annotations.append({'frame_number':frame_counter, 'annotations':annos_per_image})
            frame_counter += 1
    else:
        raise TypeError("Filename {} of unknown type".format(filename))

    return annotations
