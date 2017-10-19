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
            raise TypeError('Invalid parser %s' % fmt)
    elif issubclass(fmt, Parser):
        parser = fmt(**kwargs)
    else:
        raise TypeError('Invalid parser %s' % fmt)

    # Parse Annotations
    if parser.parser_type == ParserType.SINGLE_FILE:
        if type(anno_file) is not str:
            raise TypeError('Parser <%s> requires a single annotation file' % parser.__class__.__name__)
        with open(anno_file, 'r') as f:
            data = parser.deserialize(f.read())
    elif parser.parser_type == ParserType.MULTI_FILE:
        if type(anno_file) is not list:
            raise TypeError('Parser <%s> requires a list of annotation files' % parser.__class__.__name__)
        data = {}
        for anno in anno_file:
            img_id = os.path.splitext(os.path.basename(anno))[0]
            if img_id in data:
                raise ValueError('Multiple annotation files with the same name were found (%s)' % img_id)
            with open(anno, 'r') as f:
                data[img_id] = parser.deserialize(f.read())
    else:
        raise AttributeError('Parser <%s> has not defined a parser_type class attribute' % parser.__class__.__name__)

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
            raise TypeError('Invalid parser %s' % fmt)
    elif issubclass(fmt, Parser):
        parser = fmt(**kwargs)
    else:
        raise TypeError('Invalid parser %s' % fmt)

    # Write annotations
    if parser.parser_type == ParserType.SINGLE_FILE:
        if os.path.isdir(path):
            path = os.path.join(path, 'anno' + parser.extension)
        with open(path, 'w') as f:
            f.write(parser.serialize(anno))
    elif parser.parser_type == ParserType.MULTI_FILE:
        if not os.path.isdir(path):
            raise ValueError('Parser <%s> requires a path to a folder' % parser.__class__.__name__)
        for img_id,annos in anno.items():
            with open(os.path.join(path, img_id + parser.extension), 'w') as f:
                f.write(parser.serialize(annos))
    else:
        raise AttributeError('Parser <%s> has not defined a parser_type class attribute' % parser.__class__.__name__)
