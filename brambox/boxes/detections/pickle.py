#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Pickle detection format
#   Who doesnt want an insanely fast format
#

import pickle
from .detection import *

__all__ = ["PickleParser"]

class PickleParser(Parser):
    """ Pickle detection parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = Detection
    extension = '.pkl'
    read_mode = 'rb'
    write_mode = 'wb'

    def serialize(self, annotations):
        """ Serialize input dictionary of annotations into one string """
        result = {}
        for img_id in annotations:
            img_res = [] 
            for anno in annotations[img_id]:
                img_res.append(self.box_type.create(anno))
            result[img_id] = img_res

        return pickle.dumps(result)

    def deserialize(self, bytestream):
        """ Deserialize an annotation file into a dictionary of annotations """
        return pickle.loads(bytestream)

