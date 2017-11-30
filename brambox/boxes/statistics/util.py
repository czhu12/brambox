#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

__all__ = ['iou']


def iou(a, b):
    """Calculate the intersection over union between two boxes
    The function returns the IUO value which is defined as:
    IOU = intersection(a, b) / (area(a) + area(b) - intersection(a, b))

    a   -- first box
    b   -- second box
    """
    intersection_top_left_x = max(a.x_top_left, b.x_top_left)
    intersection_top_left_y = max(a.y_top_left, b.y_top_left)
    intersection_bottom_right_x = min(a.x_top_left + a.width,  b.x_top_left + b.width)
    intersection_bottom_right_y = min(a.y_top_left + a.height, b.y_top_left + b.height)

    intersection_width = intersection_bottom_right_x - intersection_top_left_x
    intersection_height = intersection_bottom_right_y - intersection_top_left_y

    if intersection_width <= 0 or intersection_height <= 0:
        return 0.0

    intersection_area = intersection_width * intersection_height
    union_area = a.width * a.height + b.width * b.height - intersection_area

    return intersection_area / union_area
