#
#   Copyright EAVISE
#

from enum import Enum

__all__ = ['Box', 'ParserType', 'Parser']


class Box:
    """ Generic bounding box representation """
    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        self.class_label = ''   # class string label
        self.object_id = 0      # object identifier
        self.x_top_left = 0.0   # x pixel coordinate top left of the box
        self.y_top_left = 0.0   # y pixel coordinate top left of the box
        self.width = 0.0        # width of the box in pixels
        self.height = 0.0       # height of the box in pixels
        self.ignore = False     # if true, this bounding box will not be considered in statistics processing

    @classmethod
    def create(cls, obj=None):
        """ Create a bounding box from a string or other detection object """
        instance = cls()

        if obj is None:
            return instance

        if isinstance(obj, str):
            instance.deserialize(obj)
        elif isinstance(obj, Box):
            instance.class_label = obj.class_label
            instance.object_id = obj.object_id
            instance.x_top_left = obj.x_top_left
            instance.y_top_left = obj.y_top_left
            instance.width = obj.width
            instance.height = obj.height
        else:
            raise TypeError(f'Object is not of type Box or not a string [obj.__class__.__name__]')

        return instance

    def rescale(self, value):
        self.x_top_left = self.x_top_left * value
        self.y_top_left = self.y_top_left * value
        self.width = self.width * value
        self.height = self.height * value
        return self

    def __eq__(self, other):
        # TODO: refactor: use almost equal for floats
        return self.__dict__ == other.__dict__

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
    box_type = Box                      # Derived classes should set the correct box
    extension = '.txt'                  # Derived classes should set the correct extension
    read_mode = 'r'                     # Derived classes should set the correct readmode
    write_mode = 'w'                    # Derived classes should set the correct writemode

    def __init__(self, **kwargs):
        pass

    def serialize(self, box):
        """ default serializer, can be overloaded in derived class

            The default serializer generates a text string with one box per line
            SINGLE_FILE : input dictionary {"image_id": [box, box, ...], ...} -> output string
            MULTI_FILE  : input list [box, box, ...] -> output string
            Default     : loop through annotations and call serialize
        """
        if self.parser_type != ParserType.MULTI_FILE:
            raise TypeError('The default implementation of serialize only works with MULTI_FILE')

        result = ""
        for b in box:
            new_box = self.box_type.create(b)
            result += new_box.serialize() + "\n"

        return result

    def deserialize(self, string):
        """ default deserializer, can be overloaded in derived class

            The default deserializer assumes the string contains whitespace separated values, one box per line
            SINGLE_FILE : input string -> output dictionary {"image_id": [box, box, ...], ...}
            MULTI_FILE  : input string -> output list [box, box, ...]
            Default     : loop through lines and call deserialize
        """
        if self.parser_type != ParserType.MULTI_FILE:
            raise TypeError('The default implementation of deserialize only works with MULTI_FILE')

        result = []
        for line in string.splitlines():
            result += [self.box_type.create(line)]

        return result
