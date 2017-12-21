#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Functions for modifying bounding boxes prior to analysis
#

__all__ = ['fix_aspect_ratio']


def fix_aspect_ratio(boxes, aspect_ratio=1.0):
    """Fix the aspect ratio of all bounding boxes in 'boxes' by varying the width
    of the bounding box
    boxes           -- dict with lists of boxes
    aspect_ratio    -- aspect ratio the boxes should be modified too
    """
    for image_id, values in boxes.items():
        for box in values:
            d = box.height * aspect_ratio - box.width
            box.x_top_left -= d / 2
            box.width += d
