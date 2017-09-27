#
#   Copyright EAVISE
#

from .annotation import Annotation

__all__ = ["DarknetAnnotation"]


class DarknetAnnotation(Annotation):
    """ Darknet image annotation """

    def __init__(self, obj=None, **kwargs):

        try:
            # there parameters are only present in this class for serialize/deserialize
            self.frame_width = kwargs['frame_width']
            self.frame_height = kwargs['frame_height']
        except KeyError:
            raise TypeError("Darknet annotation requires 'frame_width' and 'frame_height' keyword arguments")

        Annotation.__init__(self, obj)

        if 'frame_number' in kwargs:
            self.frame_number = kwargs['frame_number']

    def serialize(self):
        """ generate a darknet annotation string """

        # darknet format does not support 'lost' objects so there is nothing to be serialized
        if self.lost:
            return None

        x_center = self.x_top_left + self.width / 2
        y_center = self.y_top_left + self.height / 2
        x_center_relative = x_center / self.frame_width
        y_center_relative = y_center / self.frame_height
        width_relative = self.width / self.frame_width
        height_relative = self.height / self.frame_height

        string = "{} {} {} {} {}" \
            .format(self.class_label,
                    x_center_relative,
                    y_center_relative,
                    width_relative,
                    height_relative)

        return string

    def deserialize(self, string):
        """ parse a darknet annotation string """

        elements = string.split()
        self.class_label = elements[0]
        self.width = float(elements[3]) * self.frame_width
        self.height = float(elements[4]) * self.frame_height
        self.x_top_left = (float(elements[1]) * self.frame_width) - self.width / 2
        self.y_top_left = (float(elements[2]) * self.frame_height) - self.height / 2
        self.occluded = False
        self.lost = False

        return self
