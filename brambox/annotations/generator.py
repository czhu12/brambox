#
#   Copyright EAVISE
#

import os
from .formats import formats

__all__ = ["generate"]


def generate(annotations, fmt, filename, **kwargs):
    """ generate an annotation file or a set of annotation files in a specific format from a generic representation

    The function produces files and assumes the directory path mensioned in 'filename' already exist
    annotations -- annotation data
    fmt         -- format of the to be generated annotation files (string)
    filename    -- single output filename or sequence expression (containing %d) for producing multiple files
    kwargs      -- additional arguments that are forwarded to the specific annotation format class constructors
    """

    if os.path.isdir(filename):
        raise NotImplementedError

    elif os.path.isfile(filename):
        # produce a single output file
        #text = []
        #for annotation in annotations:

        #    string = formats[fmt](annotation, **kwargs).serialize()
        #    if string:
        #        text.append(string)

        #with open(filename) as f:
        #    f.write("\n".join(text))
        raise NotImplementedError

    elif '%' in filename:
        # sequence expression
        # produce a series of annotation files
        for annos_per_image in annotations:
            text = []
            for annotation in annos_per_image['annotations']:
                string = formats[fmt](annotation, **kwargs).serialize()
                if string:
                    text.append(string)

            fn = filename % annos_per_image['frame_number']
            with open(fn, 'w') as f:
                f.write("\n".join(text))

    else:
        raise TypeError("Filename {} of unknown type".format(filename))
