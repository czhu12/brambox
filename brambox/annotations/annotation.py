#
#   Copyright EAVISE
#

from enum import Enum

__all__ = ["Annotation", "Parser", "ParserType"]


class Annotation:
    """ Generic annotation representation """

    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        self.class_label = "x"  # class string label
        self.x_top_left = 0     # x pixel coordinate top left of the box
        self.y_top_left = 0     # y pixel coordinate top left of the box
        self.width = 0          # width of the box in pixels
        self.height = 0         # height of the box in pixels
        self.lost = False       # if object is not seen in the image, if true one must ignore this annotation
        self.occluded = False   # if object is occluded

    @classmethod
    def create(cls, obj=None):
        """ Create an annotation from a string or other annotation object """
        instance = cls()

        if obj is None:
            return instance

        if isinstance(obj, str):
            instance.deserialize(obj)
        elif isinstance(obj, Annotation):
            instance.class_label = obj.class_label
            instance.x_top_left = obj.x_top_left
            instance.y_top_left = obj.y_top_left
            instance.width = obj.width
            instance.height = obj.height
            instance.lost = obj.lost
            instance.occluded = obj.occluded
        else:
            raise TypeError("Object is not of type Annotation or not a string")

        return instance

    def __str__(self):
        """ pretty print """
        string = "{ "
        string += "class_label = {}, ".format(self.class_label)
        string += "x_top_left = {}, ".format(self.x_top_left)
        string += "y_top_left = {}, ".format(self.y_top_left)
        string += "width = {}, ".format(self.width)
        string += "height = {}, ".format(self.height)
        string += "lost = {}, ".format(self.lost)
        string += "occluded = {}".format(self.occluded)
        string += " }"

        return string

    def rescale(self, value):
        self.x_top_left = self.x_top_left * value
        self.y_top_left = self.y_top_left * value
        self.width = self.width * value
        self.height = self.height * value
        return self

    def serialize(self):
        """ abstract serializer, implement in derived class """
        raise NotImplementedError

    def deserialize(self, string):
        """ abstract parser, implement in derived class """
        raise NotImplementedError


class ParserType(Enum):
    """ Enum for differentiating between different parser types """
    UNDEFINED = 0
    SINGLE_FILE = 1     # One single file contains all annotations
    MULTI_FILE = 2      # One annotation file per image


class Parser:
    """ Generic parser class """
    parser_type = ParserType.UNDEFINED  # Derived classes should set the correct parser_type
    annotation_type = Annotation        # Derived classes should set the correct annotation_type
    extension = '.txt'

    def __init__(self, **kwargs):
        pass

    def serialize(self, annotations):
        """ default serializer, can be overloaded in derived class

            The default serializer generates a text string with one annotation per line
            SINGLE_FILE : input dictionary {"image_id": [anno, anno, ...], ...} -> output string
            MULTI_FILE  : input list [anno, anno, ...] -> output string
            Default     : loop through annotations and call serialize
        """
        result = ""

        for anno in annotations:
            new_anno = self.annotation_type.create(anno)
            result += new_anno.serialize() + "\n"

        return result

    def deserialize(self, string):
        """ default deserializer, can be overloaded in derived class

            The default deserializer assumes the string contains whitespace separated values, one annotation per line
            SINGLE_FILE : input string -> output dictionary {"image_id": [anno, anno, ...], ...}
            MULTI_FILE  : input string -> output list [anno, anno, ...]
            Default     : loop through lines and call deserialize
        """
        result = []

        for line in string.splitlines():
            result += [self.annotation_type.create(line)]

        return result
