#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import os

__all__ = ["expand"]


def expand(expr, stride=1, offset=0):
    """Expand a file sequence expression into multiple filenames

    A sequence expression is either:
        * a directory
        * a filename containing %d
    This function will yield all filenames found matching this expression
    """

    if os.path.isdir(expr):
        for f in sorted(os.listdir(expr)):
            if os.path.isfile(os.path.join(expr, f)):
                yield os.path.join(expr, f)

    elif '%' in expr:
        very_big_number = 10000000000
        for file_number in range(offset, very_big_number, stride):
            if file_number < 0:
                continue

            filename = expr % file_number

            if not os.path.isfile(filename):
                break

            yield filename
