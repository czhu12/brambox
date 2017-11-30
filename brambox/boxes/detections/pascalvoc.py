#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Pascal VOC detection format
#   1 file per class: img_id class_score x_left y_upper width height
#

import yaml
from .detection import *

__all__ = ["PascalVOCDetection", "PascalVOCParser"]


class PascalVOCDetection(Detection):
    """ Pascal VOC image detection """

    def serialize(self):
        """ generate a Pascal VOC detection string """
        raise NotImplementedError

    def deserialize(self, det_string, class_label):
        """ parse a Pascal VOC detection string """
        self.class_label = class_label

        elements = det_string.split()
        self.confidence = float(elements[1])
        self.x_top_left = float(elements[2])
        self.y_top_left = float(elements[3])
        self.width = float(elements[4])
        self.height = float(elements[5])

        self.object_id = 0

        return elements[0]

class PascalVOCParser(Parser):
    """ Pascal VOC detection parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = PascalVOCDetection
    extension = '.txt'

    def __init__(self, **kwargs):
        try:
            self.class_label = kwargs['class_label']
        except KeyError:
            self.class_label = ''

    def serialize(self, detections):
        """ Serialize input dictionary of detections into one string """
        raise NotImplementedError

    def deserialize(self, string):
        """ Deserialize a detection file into a dictionary of detections """
        result = {}

        for line in string.splitlines():
            if line[0] != '#':
                anno = self.box_type()
                img_id = anno.deserialize(line, self.class_label)
                if img_id in result:
                    result[img_id].append(anno)
                else:
                    result[img_id] = [anno]

        return result
