#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   YAML annotation format
#   Human readable annotation format
#
#   example file
#       img1:
#           car:
#               - coords: [x,y,w,h]
#                 lost: False
#                 occluded: True
#           person:
#               - coords: [x,y,w,h]
#                 lost: False
#                 occluded: False
#               - coords: [x,y,w,h]
#                 lost: False
#                 occluded: False
#       img2:
#           car:
#               - coords: [x,y,w,h]
#                 lost: True
#                 occluded: True
#

import yaml
from .annotation import *

__all__ = ["YamlAnnotation", "YamlParser"]


class YamlAnnotation(Annotation):
    """ YAML image annotation """

    def serialize(self):
        """ generate a yaml annotation object """
        class_label = '?' if self.class_label == '' else self.class_label
        return (class_label,
                {
                    'coords': [round(self.x_top_left), round(self.y_top_left), round(self.width), round(self.height)],
                    'lost': self.lost,
                    'occluded': self.occluded
                }
               )

    def deserialize(self, yaml_obj, class_label):
        """ parse a yaml annotation object """
        self.class_label = '' if class_label == '?' else class_label
        self.x_top_left = float(yaml_obj['coords'][0])
        self.y_top_left = float(yaml_obj['coords'][1])
        self.width = float(yaml_obj['coords'][2])
        self.height = float(yaml_obj['coords'][3])
        self.lost = yaml_obj['lost']
        self.occluded = yaml_obj['occluded']

        self.object_id = 0


class YamlParser(Parser):
    """ YAML annotation parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = YamlAnnotation
    extension = '.yaml'

    def serialize(self, annotations):
        """ Serialize input dictionary of annotations into one string """
        result = {}
        for img_id in annotations:
            img_res = {}
            for anno in annotations[img_id]:
                new_anno = self.box_type.create(anno)
                key, val = new_anno.serialize()
                if key not in img_res:
                    img_res[key] = [val]
                else:
                    img_res[key].append(val)
            result[img_id] = img_res

        return yaml.dump(result)

    def deserialize(self, string):
        """ Deserialize an annotation file into a dictionary of annotations """
        yml_obj = yaml.load(string)

        result = {}
        for img_id in yml_obj:
            anno_res = []
            for class_label, annotations in yml_obj[img_id].items():
                for anno_yml in annotations:
                    anno = self.box_type()
                    anno.deserialize(anno_yml, class_label)
                    anno_res += [anno]
            result[img_id] = anno_res

        return result
