#
#   Copyright EAVISE
#

from enum import Enum

from .. import box as b
from ..detections import detection as det

__all__ = ['Annotation', 'ParserType', 'Parser']


class Annotation(b.Box):
    """ This is a generic annotation class that provides some base functionality all annotations need.
    It builds upon :class:`~brambox.boxes.box.Box`.

    Attributes:
        lost (Boolean): Flag indicating whether the annotation is visible in the image; Default **False**
        difficult (Boolean): Flag indicating whether the annotation is considered difficult; Default **False**
        occluded (Boolean): Flag indicating whether the annotation is occluded; Default **False**
        ignore (Boolean): Flag that is used to ignore a bounding box during statistics processing; Default **False**
        visible_x_top_left (Number): X pixel coordinate of the top left corner of the bounding box that is visible; Default **0.0**
        visible_y_top_left (Number): Y pixel coordinate of the top left corner of the bounding box that is visible; Default **0.0**
        visible_width (Number): Width of the visible bounding box in pixels; Default **0.0**
        visible_height (Number): Height of the visible bounding box in pixels; Default **0.0**

    Note:
        The `visible_x_top_left`, `visible_y_top_left`, `visible_width`and `visible_height` attributes
        are only valid when the `occluded` flag is set to **True**.
    """
    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        super(Annotation, self).__init__()
        self.lost = False               # if object is not seen in the image, if true one must ignore this annotation
        self.difficult = False          # if the object is considered difficult
        self.occluded = False           # if object is occluded
        self.ignore = False             # if true, this bounding box will not be considered in statistics processing

        # variables below are only valid if the 'occluded' flag is True and
        # represent a bounding box that indicates the visible area inside the normal bounding box
        self.visible_x_top_left = 0.0   # x position top left in pixels
        self.visible_y_top_left = 0.0   # y position top left in pixels
        self.visible_width = 0.0        # width in pixels
        self.visible_height = 0.0       # height in pixels

    @classmethod
    def create(cls, obj=None):
        """ Create an annotation from a string or other box object.

        Args:
            obj (Box or string, optional): Bounding box object to copy attributes from or string to deserialize

        Note:
            The obj can be both an :class:`~brambox.boxes.annotations.Annotation` or a :class:`~brambox.boxes.detections.Detection`.
            For Annotations every attribute is copied over, for Detections the flags are all set to **False**.
        """
        instance = super(Annotation, cls).create(obj)

        if obj is None:
            return instance

        if isinstance(obj, Annotation):
            instance.lost = obj.lost
            instance.difficult = obj.difficult
            instance.occluded = obj.occluded
            instance.visible_x_top_left = obj.visible_x_top_left
            instance.visible_y_top_left = obj.visible_y_top_left
            instance.visible_width = obj.visible_width
            instance.visible_height = obj.visible_height
        elif isinstance(obj, det.Detection):
            instance.lost = False
            instance.difficult = False
            instance.occluded = False
            instance.visible_x_top_left = 0.0
            instance.visible_y_top_left = 0.0
            instance.visible_width = 0.0
            instance.visible_height = 0.0

        return instance

    def __str__(self):
        """ pretty print """
        string = 'Annotation {'
        string += f'class_label = {self.class_label}, '
        string += f'object_id = {self.object_id}, '
        string += f'x = {self.x_top_left}, '
        string += f'y = {self.y_top_left}, '
        string += f'w = {self.width}, '
        string += f'h = {self.height}, '
        string += f'ignore = {self.ignore}, '
        string += f'lost = {self.lost}, '
        string += f'occluded = {self.occluded}, '
        string += f'difficult = {self.difficult}, '
        string += f'visible_x = {self.visible_x_top_left}, '
        string += f'visible_y = {self.visible_y_top_left}, '
        string += f'visible_w = {self.visible_width}, '
        string += f'visible_h = {self.visible_height}'
        string += '}'

        return string

    __repr__ = __str__


ParserType = b.ParserType


class Parser(b.Parser):
    """ Generic parser class """
    box_type = Annotation        # Derived classes should set the correct box_type
