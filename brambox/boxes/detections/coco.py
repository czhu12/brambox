#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   NOTE: this coco format is based on the output of the darknet DL framework
#

import json
from .detection import *

__all__ = ["CocoDetection", "CocoParser"]


class CocoDetection(Detection):
    """ Json based detection format from darknet framework """

    def serialize(self):
        """ generate a json detection object """

        raise NotImplementedError

    def deserialize(self, json_obj):
        """ parse a json detection object """
        # TODO: class label map
        self.class_label = str(json_obj['category_id'])
        self.x_top_left = float(json_obj['bbox'][0])
        self.y_top_left = float(json_obj['bbox'][1])
        self.width = float(json_obj['bbox'][2])
        self.height = float(json_obj['bbox'][3])
        self.confidence = json_obj['score']

        self.object_id = 0


class CocoParser(Parser):
    """ Json based detection parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = CocoDetection
    extension = '.json'

    def serialize(self, detections):
        """ Serialize input detection to a json string"""

        raise NotImplementedError

    def deserialize(self, string):
        """ Parse a json string into a dictionary of detections """
        json_obj = json.loads(string)

        result = {}
        for json_det in json_obj:
            img_id = json_det['image_id']
            if img_id not in result:
                result[img_id] = []
            det = self.box_type()
            det.deserialize(json_det)
            result[img_id] += [det]

        return result
