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
        self.frame_number = 0
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
                    int(self.occluded == True),
                    int(self.x_top_left),
                    int(self.y_top_left),
                    int(self.x_top_left + self.width),
                    int(self.y_top_left + self.height))

        return string

    def deserialize(self, string):
        """ parse a Pascal VOC xml annotation string """
        if isinstance(string, str):
            root = ET.fromstring(string)
        else:
            raise TypeError('String parameter is not of type str %s' % type(string))

        return self.deserialize_xml(root)

    def deserialize_xml(self, xml_object):
        """ parse a Pascal VOC xml annotation object """
        if root.tag != 'object':
            root = root.find('object')
            if root is None:
                raise ValueError('Invalid xml data (no object tag was found)')

        self.class_label = root.find('name').text

        box = root.find('bndbox')
        self.x_top_left = float(box[0].text)
        self.y_top_left = float(box[1].text)
        self.width = float(int(box[2].text) - int(box[0].text))
        self.height = float(int(box[3].text) - int(box[1].text))
        self.occluded = root.find('truncated').text == '1'

        self.frame_number = 0
        self.lost = None

        return self

    @classmethod
    def deserialize_xml_multiple(cls, xml_object):
        """ Factory for producing a list of annotations for every annotation in one xml document """
        instances = []
        
        objects = xml_object.findall('object')

        for o in objects:
            anno = cls()
            anno.deserialize_xml(o)
            instances += [anno]

        return instances
