#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#

import os
from .path import expand
from ..formats import formats
from ..box import ParserType, Parser, Box

__all__ = ['parse', 'generate']


# TODO: make stride/offset work on single files
def parse(fmt, box_file, identify=None, **kwargs):
    """ Parse any type of annotation format

        fmt       : format from the brambox.boxes.format dictionary
        box_file  : bounding box filename or array of bounding box file names
        identify  : function/lambda to create an image/frame identifier based on:
                        * if single file: the parsed identifiers in the file
                        * if multi file: the filename
                    if not provided the image/frame identifier is created:
                        * if single file: by taking the parsed identifier in the file
                        * if multi file: by taking the name of the file without extension
        **kwargs  : keyword arguments that are passed to the parser
    """

    # Create parser
    if type(fmt) is str:
        try:
            parser = formats[fmt](**kwargs)
        except KeyError:
            raise TypeError(f'Invalid parser {fmt}')
    elif issubclass(fmt, Parser):
        parser = fmt(**kwargs)
    else:
        raise TypeError(f'Invalid parser {fmt}')

    # Parse bounding boxes
    if parser.parser_type == ParserType.SINGLE_FILE:
        if type(box_file) is not str:
            raise TypeError(f'Parser <{parser.__class__.__name__}> requires a single annotation file')
        with open(box_file, parser.read_mode) as f:
            data = parser.deserialize(f.read())

        # rename the image/frame ids if requested
        if identify is not None:
            data = {identify(key): value for key, value in data.items()}

    elif parser.parser_type == ParserType.MULTI_FILE:
        if type(box_file) is str:
            try:
                stride = kwargs['stride']
                offset = kwargs['offset']
            except KeyError:
                stride = 1
                offset = 0
            box_files = expand(box_file, stride, offset)
        elif type(box_file) is list:
            box_files = box_file
        else:
            raise TypeError(f'Parser <{parser.__class__.__name__}> requires a list of annotation files or an expandable file expression')

        data = {}

        # set default identify function for muti file parsers
        if identify is None:
            def identify(f): return os.path.splitext(os.path.basename(f))[0]

        for box_file in box_files:
            img_id = identify(box_file)
            if img_id in data:
                raise ValueError(f'Multiple bounding box files with the same name were found ({img_id})')

            with open(box_file, parser.read_mode) as f:
                data[img_id] = parser.deserialize(f.read())
    else:
        raise AttributeError(f'Parser <{parser.__class__.__name__}> has not defined a parser_type class attribute')

    return data


def generate(fmt, box, path, **kwargs):
    """ Generate boxtation file(s) in any format

        fmt       : format from the brambox.boxes.format dictionary
        path      : path to the boxes file (folder in case of multiple boxes)
        box       : dictionary containing box objects per image (eg. output of parse())
        **kwargs  : keyword arguments that are passed to the parser
    """

    # Create parser
    if type(fmt) is str:
        try:
            parser = formats[fmt](**kwargs)
        except KeyError:
            raise TypeError(f'Invalid parser {fmt}')
    elif issubclass(fmt, Parser):
        parser = fmt(**kwargs)
    else:
        raise TypeError(f'Invalid parser {fmt}')

    # Write bounding boxes
    if parser.parser_type == ParserType.SINGLE_FILE:
        if os.path.isdir(path):
            path = os.path.join(path, 'boxes' + parser.extension)
        with open(path, parser.write_mode) as f:
            f.write(parser.serialize(box))
    elif parser.parser_type == ParserType.MULTI_FILE:
        if not os.path.isdir(path):
            raise ValueError(f'Parser <{parser.__class__.__name__}> requires a path to a folder')
        for img_id, boxes in box.items():
            filename = os.path.join(path, img_id + parser.extension)

            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(filename, parser.write_mode) as f:
                f.write(parser.serialize(boxes))
    else:
        raise AttributeError(f'Parser <{parser.__class__.__name__}> has not defined a parser_type class attribute')
