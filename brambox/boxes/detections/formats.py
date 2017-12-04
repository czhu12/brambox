#
#   Copyright EAVISE
#

from .coco import CocoParser
from .dollar import DollarParser
from .pascalvoc import PascalVOCParser
from .pickle import PickleParser
from .yaml import YamlParser

__all__ = ['detection_formats']


detection_formats = {
    'coco': CocoParser,
    'dollar': DollarParser,
    'pascalvoc': PascalVOCParser,
    'pickle': PickleParser,
    'yaml': YamlParser,
}
