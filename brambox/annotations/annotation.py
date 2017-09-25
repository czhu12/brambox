#
#   Copyright EAVISE
#

__all__ = ["Annotation"]


class Annotation:
    """ Generic annotation representation """

    def __init__(self, obj=None):
        """ x_top_left,y_top_left,width,height are in pixel coordinates """

        if obj is not None:
            if isinstance(obj, str):
                self.deserialize(obj)
            else:
                self.frame_number = obj.frame_number
                self.class_label = obj.class_label
                self.x_top_left = obj.x_top_left
                self.y_top_left = obj.y_top_left
                self.width = obj.width
                self.height = obj.height
                self.occluded = obj.occluded

            return

        self.frame_number = 0
        self.class_label = ""
        self.x_top_left = 0.0
        self.y_top_left = 0.0
        self.width = 0.0
        self.height = 0.0
        self.occluded = False

    def __str__(self):
        """ pretty print """
        string = "{ "
        string += "frame_number = {}, ".format(self.frame_number)
        string += "class_label = {}, ".format(self.class_label)
        string += "x_top_left = {}, ".format(self.x_top_left)
        string += "y_top_left = {}, ".format(self.y_top_left)
        string += "width = {}, ".format(self.width)
        string += "height = {}, ".format(self.height)
        string += "occluded = {}".format(self.occluded)
        string += " }"

        return string

    def serialize(self):
        """ abstract serializer """

        raise NotImplementedError

    def deserialize(self, string):
        """ abstract parser """

        raise NotImplementedError
