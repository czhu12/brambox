#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   Author: Tanguy Ophoff
#
"""
These functions allow to filter out boxes depending on certain criteria.
"""


def filter_ignore(annotations, filter_fns):
    """ Set the ``ignore`` attribute of the annotations to **True** when they do not pass the provided filter functions.

    Args:
        annotations (dict or list): Dictionary containing box objects per image ``{"image_id": [box, box, ...], ...}`` or list of annotations
        filter_fns (list): List of filter functions that get applied

    Returns:
        (dict or list): boxes after filtering
    """
    if isinstance(annotations, dict):
        for _, values in annotations.items():
            for anno in values:
                if not anno.ignore:
                    for fn in filter_fns:
                        if not fn(anno):
                            anno.ignore = True
                            break
    else:
        for anno in annotations:
            if not anno.ignore:
                for fn in filter_fns:
                    if not fn(anno):
                        anno.ignore = True
                        break

    return annotations


def filter_discard(boxes, filter_fns):
    """ Delete boxes when they do not pass the provided filter functions.

    Args:
        boxes (dict or list): Dictionary containing box objects per image ``{"image_id": [box, box, ...], ...}`` or list of bounding boxes
        filter_fns (list): List of filter functions that get applied

    Returns:
        (dict or list): boxes after filtering

    Warning:
        This filter function will remove bounding boxes from your set.
        If you want to keep a copy of your original values, you should pass a copy of your bounding box dictionary:

        >>> import copy
        >>> import brambox.boxes as bbb
        >>>
        >>> new_boxes = bbb.filter_discard(copy.deepcopy(boxes), [filter_fns, ...])
    """
    if isinstance(boxes, dict):
        for image_id, values in boxes.items():
            for i in range(len(values)-1, -1, -1):
                for fn in filter_fns:
                    if not fn(values[i]):
                        del values[i]
                        break
    else:
        for i in range(len(boxes)-1, -1, -1):
            for fn in filter_fns:
                if not fn(boxes[i]):
                    del boxes[i]
                    break

    return boxes


class ImageBoundsFilter:
    """ Checks if the given box is contained in a certain area.

    Args:
        bounds (list, optional): [left, top, right, bottom] pixel positions to mark the image area; Default **[0, 0, Inf, Inf]**

    Returns:
        Boolean: **True** if the given box is entirely inside the area
    """
    def __init__(self, bounds=(0, 0, float('Inf'), float('Inf'))):
        self.bounds = bounds

    def __call__(self, box):
        return box.x_top_left >= self.bounds[0] and box.x_top_left + box.width <= self.bounds[2] and \
               box.y_top_left >= self.bounds[1] and box.y_top_left + box.height <= self.bounds[3]


class OcclusionAreaFilter:
    """ Checks if the visible fraction of an object, falls in a given range.

    Args:
        visible_range (list, optional): [min, max] ratios the visible fraction has to be in; Default **[0, Inf]**

    Returns:
        Boolean: **True** if the visible area of a bounding box divided by its total area is inside the visible range

    Note:
        The function will return **True** for boxes that are not occluded.
    """
    def __init__(self, visible_range=(0, float('Inf'))):
        self.visible_range = visible_range

    def __call__(self, box):
        if not box.occluded:
            return True

        area_visible = box.visible_width * box.visible_height
        # No visible area given -> Make sure it doesnt influence result
        if area_visible == 0 and visible_range != (0, float('Inf')):
            return False

        visible_fraction = area_visible / (box.width * box.height)
        return visible_fraction >= self.visible_range[0] and visible_fraction <= self.visible_range[1]


class HeightRangeFilter:
    """ Checks whether the height of a bounding box lies within a given range.

    Args:
        height_range (list, optional): [min, max] range for the height to be in; Default **[0, Inf]**

    Returns:
        Boolean: **True** if the height lies within the range
    """
    def __init__(self, height_range=(0, float('Inf'))):
        self.height_range = height_range

    def __call__(self, box):
        return box.height >= self.height_range[0] and box.height <= self.height_range[1]


class ClassLabelFilter:
    """ Checks whether the ``class_label`` of the box is found inside the accepted labels.

    Args:
        accepted_labels (list, optional): List of labels that should pass the filter; Default **[]**

    Returns:
        Boolean: **True** if the ``class_label`` of box is found inside the accepted labels.
    """
    def __init__(self, accepted_labels=[]):
        self.accepted_labels = accepted_labels

    def __call__(self, box):
        return box.class_label in self.accepted_labels
