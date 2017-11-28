#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import os
import glob

__all__ = ["files", "strider", "expand"]


def files(path):
    """ list all files in a directory omitting directories """
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)

def strider(elements, stride, offset):
    """ yield input elements with given stride and offset """
    next_element = offset

    # support negative offsets
    while next_element < 0:
        next_element += stride

    for i, elem in enumerate(elements):
        if i == next_element:
            next_element += stride
            yield elem

def modulo_expand(expr, stride, offset):
    """ """
    # TODO: refactor this
    very_big_number = 10000000000
    for file_number in range(offset, very_big_number, stride):
        if file_number < 0:
            continue

        filename = expr % file_number

        if not os.path.isfile(filename):
            break

        yield filename

def expand(expr, stride=1, offset=0):
    """Expand a file selection expression into multiple filenames

    A file selection expression can be:
        * a file itself (just return the filename)
        * a directory
        * a wildcard containing '*'
        * a filename containing %d
    This function will return a generator object that produces full filesnames

    expr   -- file sequence expression
    stride -- sample every n'th file where n is this parameter
    offset -- start with the m'th file where m is this parameter
    """

    if os.path.isdir(expr):
        return strider(sorted(files(expr)), stride, offset)

    elif os.path.isfile(expr):
        return expr

    elif '*' in expr:
        return strider(sorted(glob.glob(expr)), stride, offset)

    elif '%' in expr:
        return modulo_expand(expr, stride, offset)

    else:
        raise TypeError("File selection expression invalid")

