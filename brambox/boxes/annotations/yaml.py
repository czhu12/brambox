#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
"""
YAML
----
This parser generates a lightweight human readable annotation format.
With only one file for the entire dataset, this format will save you precious HDD space and will also be parsed faster.

Example:
    >>> annotations.yaml
        img1:
          car:
            - coords: [x,y,w,h]
              lost: False
              occlusion_fraction: 50.123
          person:
            - coords: [x,y,w,h]
              lost: False
              occlusion_fraction: 0.0
            - coords: [x,y,w,h]
              lost: False
              occlusion_fraction: 0.0
        img2:
          car:
            - coords: [x,y,w,h]
              lost: True
              occlusion_fraction: 90.0
"""


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
                    'occlusion_fraction': self.occlusion_fraction*100,
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

        if 'occlusion_fraction' not in yaml_obj:    # Backward compatible with older versions -> May be removed after new version is regularized
            # TODO : logging #4 (deprecation warning)
            self.occlusion_fraction = float(yaml_obj['occluded'])
        else:
            self.occlusion_fraction = yaml_obj['occlusion_fraction']/100

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
