#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

from .annotation import *

__all__ = ["CvcAnnotation", "CvcParser"]


class CvcAnnotation(Annotation):
    """ Cvc image annotation """

    def serialize(self):
        """ generate a cvc annotation string

        Note that this format does not support a class label
        """
        string = "{} {} {} {} 1 0 0 0 0 {} 0" \
            .format(round(self.x_top_left + self.width / 2),
                    round(self.y_top_left + self.height / 2),
                    round(self.width),
                    round(self.height),
                    int(self.object_id))

        return string

    def deserialize(self, string):
        """ parse a cvc annotation string

        x,y are the center of a box
        """
        elements = string.split()
        self.width = float(elements[2])
        self.height = float(elements[3])
        self.x_top_left = float(elements[0]) - self.width / 2
        self.y_top_left = float(elements[1]) - self.height / 2
        self.object_id = int(elements[9])

        self.lost = False
        self.occluded = False


class CvcParser(Parser):
    """ Cvc format annotation parser """
    parser_type = ParserType.MULTI_FILE
    box_type = CvcAnnotation
