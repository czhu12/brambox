#
#   Copyright EAVISE
#

from .formats import formats

__all__ = ["generate"]


def generate(annotations, fmt, frame_width, frame_height, filename):
    """ generate an annotation file or a set of annotation files in a specific format from a generic representation

    The function produces files and assumes the directory path mensioned in 'filename' already exist
    annotations -- annotation data
    fmt         -- format of the to be generated annotation files (string)
    filename    -- single output filename or sequence expression (containing %d) for producing multiple files
    frame_width -- needed for relative annotation formats
    frame_height -- needed for relative annotation formats
    """

    if '%' in filename:
        # produce a series of annotation files
        for frame_number, annos_per_image in enumerate(annotations):
            text = []
            for annotation in annos_per_image:
                string = formats[fmt](annotation, frame_width=frame_width,
                                        frame_height=frame_height).serialize()
                if string:
                    text.append(string)

            fn = filename % frame_number
            with open(fn, 'w') as f:
                f.write("\n".join(text))

    else:
        # produce a single output file
        text = []
        for annotation in annotations:

            string = formats[fmt](annotation, frame_width=frame_width,
                                    frame_height=frame_height).serialize()
            if string:
                text.append(string)

        with open(filename) as f:
            f.write("\n".join(text))

