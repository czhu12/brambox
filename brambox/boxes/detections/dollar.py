#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   NOTE: for parsing PeopleDetect and dollar toolbox detection output
#
"""
Dollar
------
**TODO:** Maarten
"""

from .detection import *

__all__ = ["DollarDetection", "DollarParser"]


class DollarDetection(Detection):
    """ Dollar image detection """

    def serialize(self):
        """ generate a dollar detection string """

        raise NotImplementedError

    def deserialize(self, string, class_label_map):
        """ parse a dollar detection string """
        elements = string.split(',')
        self.class_label = class_label_map[0]
        frame_nr = int(elements[0]) - 1
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = float(elements[3])
        self.height = float(elements[4])
        self.confidence = float(elements[5])

        self.object_id = 0


class DollarParser(Parser):
    """ Dollar detection format parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = DollarDetection

    def __init__(self, **kwargs):
        """ Only the first element of the class label map is used since this format
            does not support class labels
        """
        try:
            self.class_label_map = kwargs['class_label_map']
        except KeyError:
            raise TypeError("Dollar detection format requires 'class_label_map' keyword arguments")

    def serialize(self, detections):
        """ Serialize input detection to dollar detection strings """

        raise NotImplementedError

    def deserialize(self, string):
        """ Parse a json string into a dictionary of detections """
        result = {}
        for line in string.splitlines():
            img_id = str(int(line.split(',')[0]) - 1)
            if img_id not in result:
                result[img_id] = []
            det = self.box_type()
            det.deserialize(line, self.class_label_map)
            result[img_id] += [det]

        return result
