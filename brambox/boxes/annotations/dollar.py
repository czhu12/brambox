#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
"""
Dollar
------
**TODO:** Maarten
"""

from .annotation import *

__all__ = ["DollarAnnotation", "DollarParser"]


class DollarAnnotation(Annotation):
    """ Dollar image annotation """

    def serialize(self):
        """ generate a dollar annotation string """
        string = "{} {} {} {} {} {} {} {} {} {} {} 0" \
            .format(self.class_label if len(self.class_label) != 0 else '?',
                    round(self.x_top_left),
                    round(self.y_top_left),
                    round(self.width),
                    round(self.height),
                    int(self.occluded),
                    round(self.visible_x_top_left),
                    round(self.visible_y_top_left),
                    round(self.visible_width),
                    round(self.visible_height),
                    int(self.lost))

        return string

    def deserialize(self, string, occlusion_tag_map):
        """ parse a dollar annotation string """
        elements = string.split()
        self.class_label = '' if elements[0] == '?' else elements[0]
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = float(elements[3])
        self.height = float(elements[4])
        if occlusion_tag_map is None:
            self.occluded = elements[5] != '0'
        else:
            self.occlusion_fraction = occlusion_tag_map[int(elements[5])]
        self.visible_x_top_left = float(elements[6])
        self.visible_y_top_left = float(elements[7])
        self.visible_width = float(elements[8])
        self.visible_height = float(elements[9])
        self.lost = elements[10] != '0'

        self.object_id = 0

        return self


class DollarParser(Parser):
    """ Dollar format annotation parser """
    parser_type = ParserType.MULTI_FILE
    box_type = DollarAnnotation

    def __init__(self, **kwargs):
        self.occlusion_tag_map = None
        if 'occlusion_tag_map' in kwargs:
            self.occlusion_tag_map = kwargs['occlusion_tag_map']

    def deserialize(self, string):
        """ deserialize a dollar string into a list of annotations

        This deserializer checks for header/comment strings in dollar strings
        """
        result = []

        for line in string.splitlines():
            if '%' not in line:
                anno = self.box_type()
                result += [anno.deserialize(line, self.occlusion_tag_map)]

        return result
