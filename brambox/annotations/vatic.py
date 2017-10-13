#
#   Copyright EAVISE
#

from .annotation import Annotation

__all__ = ["VaticAnnotation"]


class VaticAnnotation(Annotation):
    """ VATIC tool annotation """

    def __init__(self, obj=None, **kwargs):

        if 'frame_number' in kwargs:
            self.frame_number = kwargs['frame_number']

        Annotation.__init__(self, obj)

    def serialize(self):
        """ generate a vatic annotation string """

        object_id = 0
        x_min = round(self.x_top_left)
        y_min = round(self.y_top_left)
        x_max = round(self.x_top_left + self.width)
        y_max = round(self.y_top_left + self.height)
        frame_nr = self.frame_number
        lost = int(self.lost)
        occluded = int(self.occluded)
        generated = 0
        class_label = self.class_label

        string = "{} {} {} {} {} {} {} {} {} {}" \
            .format(object_id,
                    x_min,
                    y_min,
                    x_max,
                    y_max,
                    frame_nr,
                    lost,
                    occluded,
                    generated,
                    class_label)

        return string

    def deserialize(self, string):
        """ parse a valitc annotation """

        elements = string.split()
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = abs(float(elements[3]) - self.x_top_left)
        self.height = abs(float(elements[4]) - self.y_top_left)
        self.frame_number = int(elements[5])
        self.lost = elements[6] != '0'
        self.occluded = elements[7] != '0'
        self.class_label = elements[9].strip('\"')

        return self
