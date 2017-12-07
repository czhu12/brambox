#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

__all__ = ['iou', 'iob']

def intersection(a, b):
    """Calculate the intersection area between two boxes
    """
    intersection_top_left_x = max(a.x_top_left, b.x_top_left)
    intersection_top_left_y = max(a.y_top_left, b.y_top_left)
    intersection_bottom_right_x = min(a.x_top_left + a.width,  b.x_top_left + b.width)
    intersection_bottom_right_y = min(a.y_top_left + a.height, b.y_top_left + b.height)

    intersection_width = intersection_bottom_right_x - intersection_top_left_x
    intersection_height = intersection_bottom_right_y - intersection_top_left_y

    if intersection_width <= 0 or intersection_height <= 0:
        return 0.0

    return intersection_width * intersection_height

def iou(a, b):
    """Calculate the intersection over union between two boxes
    The function returns the IUO value which is defined as:
    IOU = intersection(a, b) / (area(a) + area(b) - intersection(a, b))

    a   -- first box
    b   -- second box
    """
    intersection_area = intersection(a, b)
    union_area = a.width * a.height + b.width * b.height - intersection_area

    return intersection_area / union_area

def iob(a, b):
    """Calculate the intersection over b between two boxes
    The function returns the value which is defined as:
    IOB = intersection(a, b) / (area(b))
    """
    return intersection(a, b) / (b.width * b.height)
