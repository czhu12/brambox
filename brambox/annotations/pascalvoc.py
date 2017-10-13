#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import xml.etree.ElementTree as ET

from .annotation import Annotation

__all__ = ["PascalVOCAnnotation"]


class PascalVOCAnnotation(Annotation):
    """ Pascal VOC image annotation """

    def __init__(self, obj=None, **kwargs):
        self.lost = False
        Annotation.__init__(self, obj)

    def serialize(self):
        """ generate a Pascal VOC object xml string """

        string = ("<object>\n"
                  "<name>{}</name>\n"
                  "<pose>Unspecified</pose>\n"
                  "<truncated>{}</truncated>\n"
                  "<difficult>0</difficult>\n"
                  "<bndbox>\n"
                  "<xmin>{}</xmin>\n"
                  "<ymin>{}</ymin>\n"
                  "<xmax>{}</xmax>\n"
                  "<ymay>{}</ymay>\n"
                  "</bndbox>\n"
                  "</object>\n") \
            .format(self.class_label,
                    1 if self.occluded else 0,
                    int(self.x_top_left),
                    int(self.y_top_left),
                    int(self.x_top_left + self.width),
                    int(self.y_top_left + self.height))

        return string

    def deserialize(self, string):
        """ parse a Pascal VOC xml annotation object/string """

        if isinstance(string, str):
            root = ET.fromstring(string)
        else:
            root = string

        if root.tag != 'object':
            root = root.find('object')
            assert root is not None, 'Invalid xml data (no object tag was found)'

        self.class_label = root.find('name').text

        box = root.find('bndbox')
        self.x_top_left = float(box[0].text)
        self.y_top_left = float(box[1].text)
        self.width = float(int(box[2].text) - int(box[0].text))
        self.height = float(int(box[3].text) - int(box[1].text))
        self.occluded = root.find('truncated').text == '1'

        self.lost = None

        return self
