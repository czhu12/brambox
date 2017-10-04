#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

from .annotation import Annotation

__all__ = ["DarknetAnnotation"]


class DarknetAnnotation(Annotation):
    """ Darknet image annotation """

    def __init__(self, img_width, img_height, obj=None):
        self.img_width = img_width
        self.img_height = img_height

        self.frame_number = 0
        self.lost = False
        self.occluded = False
        Annotation.__init__(self, obj)

    def serialize(self):
        """ generate a darknet annotation string """

        x_center = (self.x_top_left + self.width / 2) / self.img_width
        y_center = (self.y_top_left + self.height / 2) / self.img_height
        w = self.width / self.img_width
        h = self.height / self.img_height

        string = "{} {} {} {} {}" \
            .format(self.class_label,
                    x_center,
                    y_center,
                    w,
                    h)

        return string

    def deserialize(self, string):
        """ parse a darknet annotation string """

        elements = string.split()
        self.class_label = elements[0]
        self.width = float(elements[3]) * self.img_width
        self.height = float(elements[4]) * self.img_height
        self.x_top_left = float(elements[1]) * self.img_width - self.width / 2
        self.y_top_left = float(elements[2]) * self.img_height - self.height / 2

        self.frame_number = 0
        self.occluded = False
        self.lost = False

        return self

