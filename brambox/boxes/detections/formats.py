#
#   Copyright EAVISE
#

from .coco import CocoParser
from .pascalvoc import PascalVOCParser
from .pickle import PickleParser
from .yaml import YamlParser

__all__ = ['detection_formats']


detection_formats = {
    'coco': CocoParser,
    'pascalvoc': PascalVOCParser,
    'pickle': PickleParser,
    'yaml': YamlParser,
}
