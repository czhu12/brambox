#
#   Copyright EAVISE
#

from .annotation import Annotation

__all__ = ["DollarAnnotation"]


class DollarAnnotation(Annotation):
    """ Dollar image annotation """

    def __init__(self, obj=None, **kwargs):
        Annotation.__init__(self, obj)

        if 'frame_number' in kwargs:
            self.frame_number = kwargs['frame_number']

    def serialize(self):
        """ generate a dollar annotation string """

        string = "{} {} {} {} {} {} 0 0 0 0 {} 0" \
            .format(self.class_label,
                    round(self.x_top_left),
                    round(self.y_top_left),
                    round(self.width),
                    round(self.height),
                    int(self.occluded),
                    int(self.lost))

        return string

    def deserialize(self, string):
        """ parse a dollar annotation string """

        elements = string.split()
        self.class_label = elements[0]
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = float(elements[3])
        self.height = float(elements[4])
        self.occluded = elements[5] != '0'
        self.lost = elements[10] != '0'

        return self
