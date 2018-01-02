#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   Author: Tanguy Ophoff
#
"""
These functions allow to filter out boxes depending on certain criteria.
"""


def filter_ignore(annotations, filter_fn, *args, **kwargs):
    """ Set the ``ignore`` attribute of the annotations to **True** when they do not pass the provided filter function.

    Args:
        annotations (dict): Dictionary containing box objects per image ``{"image_id": [box, box, ...], ...}``
        filter_fn (function): Filter function that gets applied
        *args: Arguments for the filter function
        **kwargs: Keyword arguments for the filter function
    """
    for _, values in annotations.items():
        for anno in values:
            if not anno.ignore and not filter_fn(anno, *args, **kwargs):
                anno.ignore = True


def filter_discard(boxes, filter_fn, *args, **kwargs):
    """ Delete boxes when they do not pass the provided filter function.

    Args:
        boxes (dict): Dictionary containing box objects per image ``{"image_id": [box, box, ...], ...}``
        filter_fn (function): Filter function that gets applied
        *args: Arguments for the filter function
        **kwargs: Keyword arguments for the filter function
    """

    for image_id, values in boxes.items():
        values[:] = [box for box in values if filter_fn(box, *args, **kwargs)]


def image_bounds_filter(box, bounds=(0, 0, float('Inf'), float('Inf'))):
    """ Checks if the given box is contained in a certain area.

    Args:
        box (brambox.boxes.Box): Box to check
        bounds (list, optional): [left, top, right, bottom] pixel positions to mark the image area; Default **[0, 0, Inf, Inf]**

    Returns:
        Boolean: **True** if the given box is entirely inside the area
    """
    return box.x_top_left >= bounds[0] and box.x_top_left + box.width <= bounds[2] and \
        box.y_top_left >= bounds[1] and box.y_top_left + box.height <= bounds[3]


def occlusion_area_filter(box, visible_range=(0, float('Inf'))):
    """ Checks if the visible fraction of an object, falls in a given range.

    Args:
        box (brambox.boxes.Box): Box to check
        visible_range (list, optional): [min, max] ratios the visible fraction has to be in; Default **[0, Inf]**

    Returns:
        Boolean: **True** if the visible area of a bounding box divided by its total area is inside the visible range

    Note:
        The function will return **True** for boxes that are not occluded.
    """
    if not box.occluded:
        return True

    area_visible = box.visible_width * box.visible_height
    # No visible area given -> Make sure it doesnt influence result
    # TODO: rework visible
    if area_visible == 0:
        return False

    visible_fraction = area_visible / (box.width * box.height)
    return visible_fraction >= visible_range[0] and visible_fraction <= visible_range[1]


def height_range_filter(box, height_range=(0, float('Inf'))):
    """ Checks whether the height of a bounding box lies within a given range.

    Args:
        box (brambox.boxes.Box): Box to check
        visible_range (list, optional): [min, max] range for the height to be in; Default **[0, Inf]**

    Returns:
        Boolean: **True** if the height lies within the range
    """
    return box.height >= height_range[0] and box.height <= height_range[1]


# NOTE: Is this useful? height_range can already fullfill this...
def expanded_height_range(box, height_range=(0, float('Inf')), r=1.25):
    # Return True if the height of a given box lies within the given range after scaling the range with 'r'
    # box             -- box object to test
    # height_range    -- height range in pixels
    # r               -- scaling factor that is first applied to the range before comparison
    expanded_range = (height_range[0] / r, height_range[1] * r)
    return box.height >= expanded_range[0] and box.height <= expanded_range[1]


def label_filter(box, accepted_labels=[]):
    """ Checks whether the ``class_label`` of the box is found inside the accepted labels.

    Args:
        box (brambox.boxes.Box): Box to check
        accepted_labels (list, optional): List of labels that should pass the filter; Default **[]**

    Returns:
        Boolean: **True** if the ``class_label`` of box is found inside the accepted labels.
    """
    return box.class_label in accepted_labels
