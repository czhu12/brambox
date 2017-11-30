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
        raise NotImplementedError

    def deserialize(self, string):
        """ parse a Pascal VOC xml annotation string """
        raise NotImplementedError


class PascalVOCParser(Parser):
    """ YAML annotation parser """
    parser_type = ParserType.MULTI_FILE
    box_type = PascalVOCAnnotation
    extension = '.xml'

    def serialize(self, annotations):
        """ Serialize input dictionary of annotations into one string """
        raise NotImplementedError

    def deserialize(self, string):
        """ Deserialize an annotation file into a dictionary of annotations """
        raise NotImplementedError
