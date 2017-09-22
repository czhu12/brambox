#
#   Copyright EAVISE
#

__all__ = ["VaticAnnotation"]


class VaticAnnotation:
    """ VATIC annotation tool output format """

    def __init__(self, string):
        self.deserialize(string)

    def serialize(self):
        """ generate a vatic annotation string """

        raise NotImplementedError

    def deserialize(self, string):
        """ parse a valitc annotation """

        elements = string.split()
        self.identifier = int(elements[0])
        self.x_min = int(elements[1])
        self.y_min = int(elements[2])
        self.x_max = int(elements[3])
        self.y_max = int(elements[4])
        self.frame_number = int(elements[5])
        self.lost = int(elements[6])
        self.occluded = int(elements[7])
        self.generated = int(elements[8])
        self.class_label = elements[9]
