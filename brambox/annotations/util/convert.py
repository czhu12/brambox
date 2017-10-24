#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#

import os
from ..formats import formats
from ..annotation import ParserType, Parser, Annotation

__all__ = ['parse', 'generate']

def parse(fmt, anno_file, **kwargs):
    """ Parse any type of annotation format
        
        fmt       : format from the brambox.annotations.format dictionary
        anno_file : annotation filename or array of annotation file names
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

    # Parse Annotations
    if parser.parser_type == ParserType.SINGLE_FILE:
        if type(anno_file) is not str:
            raise TypeError(f'Parser <{parser.__class__.__name__}> requires a single annotation file')
        with open(anno_file, 'r') as f:
            data = parser.deserialize(f.read())
    elif parser.parser_type == ParserType.MULTI_FILE:
        if type(anno_file) is not list:
            raise TypeError(f'Parser <{parser.__class__.__name__}> requires a list of annotation files')
        data = {}
        for anno in anno_file:
            img_id = os.path.splitext(os.path.basename(anno))[0]
            if img_id in data:
                raise ValueError(f'Multiple annotation files with the same name were found ({img_id})')
            with open(anno, 'r') as f:
                data[img_id] = parser.deserialize(f.read())
    else:
        raise AttributeError(f'Parser <{parser.__class__.__name__}> has not defined a parser_type class attribute')

    return data

def generate(fmt, anno, path, **kwargs):
    """ Generate annotation file(s) in any format
        
        fmt       : format from the brambox.annotations.format dictionary
        path      : path to the annotation file (folder in case of multiple annotations)
        anno      : dictionary containing annotation objects per image (eg. output of parse())
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

    # Write annotations
    if parser.parser_type == ParserType.SINGLE_FILE:
        if os.path.isdir(path):
            path = os.path.join(path, 'anno' + parser.extension)
        with open(path, 'w') as f:
            f.write(parser.serialize(anno))
    elif parser.parser_type == ParserType.MULTI_FILE:
        if not os.path.isdir(path):
            raise ValueError(f'Parser <{parser.__class__.__name__}> requires a path to a folder')
        for img_id,annos in anno.items():
            with open(os.path.join(path, img_id + parser.extension), 'w') as f:
                f.write(parser.serialize(annos))
    else:
        raise AttributeError(f'Parser <{parser.__class__.__name__}> has not defined a parser_type class attribute')
