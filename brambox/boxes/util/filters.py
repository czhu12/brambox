#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Functions for filtering bounding boxes prior to generating curve data
#


def image_bounds(box, bounds=(0, 0, float('Inf'), float('Inf')), image_size=(100, 100)):
    """Return True if the given box does not overlap the given image bounds
    box         -- box object to test
    bounds      -- [top, left, bottom, right] pixel positions to mark the image bounds
    image_size  -- image size in pixels (width, height)
    """
    raise NotImplementedError


def occlusion_area(box, min_visible_area=0):
    """Return True if the visible area of the given box is equal or greater than a certain minimum
    If the object is equal or more occluded than given by the occlusion ratio, it will be ignored
    box                 -- box object to test
    min_visible_area    -- minimum visible area
    """
    # TODO: visible area not yet implemented in boxes package
    raise NotImplementedError


def height_range(box, range=(0, float('Inf'))):
    """Return True if the height of a given box lies within the given range
    box         -- box object to test
    range       -- height range in pixels (lower, upper)
    """
    return box.height >= range[0] and box.height <= range[1]


def extended_height_range(box, range=(0, float('Inf')), r=1.25):
    """Return True if the height of a given box lies within the given range after scaling
    the height of the box with 'r'
    box         -- box object to test
    range       -- height range in pixels
    r           -- scaling factor that is first applied to the box before checking its range
    """
    # check if range needs to be scaled or the box's height
    raise NotImplementedError


def filter_boxes(boxes, filters=[], **kwargs):
    """Mark boxes as 'ignore' when they to not pass the provided filter functions
    boxes       -- list or dict with lists of boxes
    filters     -- a list of filter functions to be applied
    """
