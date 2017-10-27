#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import os

__all__ = ["files", "expand"]

def files(path):
    """ list all files in a directory """
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield os.path.join(path, file)

def expand(expr, stride=1, offset=0):
    """Expand a file sequence expression into multiple filenames

    A sequence expression is either:
        * a directory
        * a filename containing %d
    This function will yield all filenames found matching this expression

    expr   -- file sequence expression
    stride -- sample every n'th file where n is this parameter
    offset -- start with the m'th file where m is this parameter
    """

    if os.path.isdir(expr):
        next_file_number = offset

        # support negative offsets
        while next_file_number < 0:
            next_file_number += stride

        for i, file in enumerate(sorted(files(expr))):
            if i == next_file_number:
                next_file_number += stride
                yield file

    elif '%' in expr:
        # TODO: refactor this
        very_big_number = 10000000000
        for file_number in range(offset, very_big_number, stride):
            if file_number < 0:
                continue

            filename = expr % file_number

            if not os.path.isfile(filename):
                break

            yield filename
