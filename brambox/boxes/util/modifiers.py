#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   Author: Tanguy Ophoff
#
"""
These modifier functions allow to change certain aspects of your annotations and detections.
"""


def modify(boxes, modifier_fns):
    """ Modifies boxes according to the modifier functions.

    Args:
        annotations (dict): Dictionary containing box objects per image ``{"image_id": [box, box, ...], ...}``
        modifier_fns (list): List of modifier functions that get applied
    """
    for _, values in boxes.items():
        for i in range(len(values)):
            for fn in modifier_fns:
                values[i] = fn(values[i])

    return boxes


class AspectRatio_modifier:
    """ Change the aspect ratio of all bounding boxes in ``boxes``.

    Args:
        aspect_ratio (Number, optional): Target aspect ratio, defined as height/width; Default **1.0**
        change (str, optional): which length to change; Default **'width'**

    Note:
        The ``change`` parameter can be one of 4 different values.
        If the parameter is **'width'**, then the width of the bounding box will be modified to reach the new aspect ratio.
        If it is **'height'**, then the height of the bounding box will be modified. |br|
        If the parameter is **'reduce'**, then the bounding box will be cropped to reach the new aspect ratio.
        If it is **'enlarge'**, then the bounding box will be made bigger.
    """
    def __init__(self, aspect_ratio=1.0, change='width', modify_ignores=False):
        self.ar = aspect_ratio
        self.modify_ignores = modify_ignores
        change = change.lower()
        if change == 'reduce':
            self.change = 0
        elif change == 'enlarge':
            self.change = 1
        elif change == 'height':
            self.change = 2
        else:
            self.change = 3

    def __call__(self, box):
        if not self.modify_ignores and hasattr(box, 'ignore') and box.ignore:
            return box

        change = False
        if self.change == 0:
            if box.height / box.width > self.ar:
                change = True
        elif self.change == 1:
            if box.height / box.width < self.ar:
                change = True

        if self.change == 2 or change:
            d = box.width * self.ar - box.height
            box.y_top_left -= d / 2
            box.height += d
        else:
            d = box.height * self.ar - box.width
            box.x_top_left -= d / 2
            box.width += d

        return box


class Scale_modifier:
    """ Rescale your bounding boxes like you would rescale an image.

    Args:
        scale (Number or list): Value to rescale your bounding box, defined as a single number or a (width, height) tuple
    """
    def __init__(self, scale):
        if isinstance(scale, int):
            self.scale = (scale, scale)
        else:
            self.scale = tuple(scale[:2])

    def __call__(self, box):
        box.x_top_left *= self.scale[0]
        box.y_top_left *= self.scale[1]
        box.width *= self.scale[0]
        box.height *= self.scale[1]

        return box
