#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#

from .annotation import *

__all__ = ["DarknetAnnotation", "DarknetParser"]


class DarknetAnnotation(Annotation):
    """ Darknet image annotation """

    def serialize(self, class_label_map, image_width, image_height):
        """ generate a darknet annotation string """
        if class_label_map is not None:
            class_label_index = class_label_map.index(self.class_label)
        else:
            class_label_index = 0

        x_center = self.x_top_left + float(self.width) / 2
        y_center = self.y_top_left + float(self.height) / 2
        x_center_relative = x_center / image_width
        y_center_relative = y_center / image_height
        width_relative = float(self.width) / image_width
        height_relative = float(self.height) / image_height

        string = "{} {} {} {} {}" \
            .format(class_label_index,
                    x_center_relative,
                    y_center_relative,
                    width_relative,
                    height_relative)

        return string

    def deserialize(self, string, class_label_map, image_width, image_height):
        """ parse a darknet annotation string """
        elements = string.split()
        if class_label_map is not None:
            self.class_label = class_label_map[int(elements[0])]
        else
            self.class_label = int(elements[0])

        self.width = float(elements[3]) * image_width
        self.height = float(elements[4]) * image_height
        self.x_top_left = float(elements[1]) * image_width - self.width / 2
        self.y_top_left = float(elements[2]) * image_height - self.height / 2

        self.occluded = False
        self.lost = False
        self.object_id = 0

        return self


class DarknetParser(Parser):
    """ Darknet annotation parser """
    parser_type = ParserType.MULTI_FILE     # Darknet annotations have one file per image
    annotation_type = DarknetAnnotation     # Darknet annotation type

    def __init__(self, **kwargs):
        try:
            self.image_width = kwargs['image_width']
            self.image_height = kwargs['image_height']
            self.class_label_map = kwargs['class_label_map']
        except KeyError:
            raise TypeError("Darknet parser requires 'image_width', 'image_height' and 'class_label_map' keyword arguments")

        if self.image_width is None:
            raise TypeError("Darknet parser requires image_width")
        if self.image_height is None:
            raise TypeError("Darknet parser requires image_height")

    def serialize(self, annotations):
        """ Serialize a list of annotations into one string """
        result = ""

        for anno in annotations:
            if anno.lost:   # darknet does not support lost type -> ignore
                continue
            new_anno = self.annotation_type.create(anno)
            result += new_anno.serialize(self.class_label_map, self.image_width, self.image_height) + "\n"

        return result

    def deserialize(self, string):
        """ Deserialize an annotation string into a list of annotation """
        result = []

        string = string.splitlines()
        for line in string:
            anno = self.annotation_type()
            result += [anno.deserialize(line, self.class_label_map, self.image_width, self.image_height)]

        return result
