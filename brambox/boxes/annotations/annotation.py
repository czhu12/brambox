#
#   Copyright EAVISE
#

from enum import Enum

from .. import box as b
from ..detections import detection as det

__all__ = ['Annotation', 'ParserType', 'Parser']


class Annotation(b.Box):
    """ Generic annotation representation """
    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        super(Annotation, self).__init__()
        self.lost = False       # if object is not seen in the image, if true one must ignore this annotation
        self.occluded = False   # if object is occluded

    @classmethod
    def create(cls, obj=None):
        """ Create an annotation from a string or other box object """
        instance = super(Annotation, cls).create(obj)

        if obj is None:
            return instance

        if isinstance(obj, Annotation):
            instance.lost = obj.lost
            instance.occluded = obj.occluded
        elif isinstance(obj, det.Detection):
            instance.lost = False
            instance.occluded = False

        return instance

    def __str__(self):
        """ pretty print """
        string = "Annotation { "
        string += "\tclass_label = {self.class_label}, "
        string += "\tobject_id = {self.object_id}, "
        string += "\tx_top_left = {self.x_top_left}, "
        string += "\ty_top_left = {self.y_top_left}, "
        string += "\twidth = {self.width}, "
        string += "\theight = {self.height}, "
        string += "\tignore = {self.ignore}, "
        string += "\tlost = {self.lost}, "
        string += "\toccluded = {self.occluded}"
        string += "}"

        return string


ParserType = b.ParserType


class Parser(b.Parser):
    """ Generic parser class """
    box_type = Annotation        # Derived classes should set the correct box_type
