#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

from .annotation import *

__all__ = ["DollarAnnotation", "DollarParser"]


class DollarAnnotation(Annotation):
    """ Dollar image annotation """

    def serialize(self):
        """ generate a dollar annotation string """
        string = "{} {} {} {} {} {} 0 0 0 0 {} 0" \
            .format(self.class_label if len(self.class_label) != 0 else '?',
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
        self.class_label = '' if elements[0] == '?' else elements[0] 
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = float(elements[3])
        self.height = float(elements[4])
        self.occluded = elements[5] != '0'
        self.lost = elements[10] != '0'

        self.object_id = 0


class DollarParser(Parser):
    """ Dollar format annotation parser """
    parser_type = ParserType.MULTI_FILE
    box_type = DollarAnnotation

    def deserialize(self, string):
        """ deserialize a dollar string into a list of annotations

        This deserializer checks for header/comment strings in dollar strings
        """
        result = []

        for line in string.splitlines():
            if '%' not in line:
                result += [self.box_type.create(line)]

        return result
