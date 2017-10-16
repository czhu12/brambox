#
#   Copyright EAVISE
#

__all__ = ["Annotation", "Parser"]


class Annotation:
    """ Generic annotation representation """

    def __init__(self):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """
        self.frame_number = 0   # frame number this annotation belongs to starting with 0
        self.class_label = "x"  # class string label
        self.x_top_left = 0.0   # x pixel coordinate top left of the box
        self.y_top_left = 0.0   # y pixel coordinate top left of the box
        self.width = 0.0        # width of the box in pixels
        self.height = 0.0       # height of the box in pixels
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

    def serialize(self):
        """ abstract serializer, implement in derived class """
        raise NotImplementedError

    def deserialize(self, string):
        """ abstract parser, implement in derived class """
        raise NotImplementedError

class Parser:
    """ Generic parser class """

    def __init__(self):
        pass

    def serialize(self, annotations):
        """ abstract serializer, implement in derived class
            Default : loop through annotations and call serialize """
        result = []
        for anno in annotations:
            result += [anno.serialize()]
        return result

    def deserialize(self, chunk):
        """ abstract deserializer, implement in derived class
            Default : loop through lines and call deserialize """
        result = []
        for line in chunk:
            result += [anno.deserialize(line)]
        return result
