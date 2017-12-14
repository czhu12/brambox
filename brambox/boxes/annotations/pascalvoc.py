#
#   Copyright EAVISE
#   By Tanguy Ophoff
#   TODO : Not converted to new style
#

import xml.etree.ElementTree as ET

from .annotation import *

__all__ = ['PascalVOCAnnotation', 'PascalVOCParser']


class PascalVOCAnnotation(Annotation):
    """ Pascal VOC image annotation """

    def serialize(self):
        """ generate a Pascal VOC object xml string """
        string = '<object>\n'
        string += f'\t<name>{self.class_label}</name>\n'
        string += '\t<pose>Unspecified</pose>\n'
        string += f'\t<truncated>{int(self.occluded)}</truncated>\n'
        string += '\t<difficult>0</difficult>\n'
        string += '\t<bndbox>\n'
        string += f'\t\t<xmin>{self.x_top_left}</xmin>\n'
        string += f'\t\t<ymin>{self.y_top_left}</ymin>\n'
        string += f'\t\t<xmax>{self.x_top_left + self.width}</xmax>\n'
        string += f'\t\t<ymax>{self.y_top_left + self.height}</ymax>\n'
        string += '\t</bndbox>\n'
        string += '</object>\n'

        return string

    def deserialize(self, xml_obj):
        """ parse a Pascal VOC xml annotation string """
        self.class_label = xml_obj.find('name').text
        self.occluded = xml_obj.find('truncated').text == '1'

        box = xml_obj.find('bndbox')
        self.x_top_left = float(box.find('xmin').text)
        self.y_top_left = float(box.find('ymin').text)
        self.width = float(int(box.find('xmax').text) - self.x_top_left)
        self.height = float(int(box.find('ymax').text) - self.y_top_left)

        self.object_id = 0
        self.lost = None

        return self


class PascalVOCParser(Parser):
    """ Pascal VOC annotation parser """
    parser_type = ParserType.MULTI_FILE
    box_type = PascalVOCAnnotation
    extension = '.xml'

    def serialize(self, annotations):
        """ Serialize a list of annotations into one string """
        result = '<annotation>\n'

        for anno in annotations:
            new_anno = self.box_type.create(anno)
            result += new_anno.serialize()

        return result + '</annotation>\n'

    def deserialize(self, string):
        """ Deserialize an annotation string into a list of annotation """
        result = []

        root = ET.fromstring(string)
        for obj in root.iter('object'):
            anno = self.box_type()
            result += [anno.deserialize(obj)]

        return result
