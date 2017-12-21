#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Functions for filtering bounding boxes prior to generating curve data
#

__all__ = ['image_bounds', 'occlusion_area', 'height_range', 'expanded_height_range',
            'label', 'filter_ignore', 'filter_discard']


def image_bounds(box, bounds=(0, 0, float('Inf'), float('Inf'))):
    """Return True if the given box does not overlap the given image bounds
    box         -- box object to test
    bounds      -- [left, top, right, bottom] pixel positions to mark the image bounds
    """
    return box.x_top_left >= bounds[0] and box.x_top_left + box.width <= bounds[2] and \
           box.y_top_left >= bounds[1] and box.y_top_left + box.height <= bounds[3]

def occlusion_area(box, visible_range=(0, float('Inf'))):
    """Return True if the visible fraction of an object, denotated by a bouding box, falls between
    a given visible range.
    If the object is equal or more occluded than given by the occlusion ratio, it will be ignored
    box                 -- box object to test
    visible_range       -- visible fraction range
    """
    if not box.occluded:
        return True

    area_visible = box.visible_width * box.visible_height

    # if no visible area was given, we don't know how mutch the object is occluded so
    # make sure it does not influence the result
    if area_visible == 0:
        return False

    visible_fraction = area_visible / (box.width * box.height)

    return visible_fraction >= visible_range[0] and visible_fraction <= visible_range[1]

def height_range(box, height_range=(0, float('Inf'))):
    """Return True if the height of a given box lies within the given range
    box             -- box object to test
    height_range    -- height range in pixels (lower, upper)
    """
    return box.height >= height_range[0] and box.height <= height_range[1]

def expanded_height_range(box, height_range=(0, float('Inf')), r=1.25):
    """Return True if the height of a given box lies within the given range after scaling
    the range with 'r'
    box             -- box object to test
    height_range    -- height range in pixels
    r               -- scaling factor that is first applied to the range before comparison
    """
    expanded_range = (height_range[0] / r, height_range[1] * r)
    return box.height >= expanded_range[0] and box.height <= expanded_range[1]

def label(box, accepted_labels=[]):
    """Return True if the 'class_label' of 'box' is found inside the 'acceted_labels'
    box             -- box object to test
    accepted_labels -- list of labels that should pass the filter
    """
    return box.class_label in accepted_labels

def filter_ignore(boxes, filter_fun, *args, **kwargs):
    """Mark boxes as 'ignore' when they do not pass the provided filter function
    boxes       -- dict with lists of boxes
    filter_fun  -- a filter function to be applied
    """

    for image_id, values in boxes.items():
        for box in values:
            if not box.ignore and not filter_fun(box, *args, **kwargs):
                box.ignore = True


def filter_discard(boxes, filter_fun, *args, **kwargs):
    """Delete boxes when they do not pass the provided filter function
    boxes       -- dict with lists of boxes
    filter_fun  -- a filter function to be applied
    """

    for image_id, values in boxes.items():
        values[:] = [box for box in values if filter_fun(box, *args, **kwargs)]

