#
#   Copyright EAVISE
#

from .coco import CocoParser
from .pickle import PickleParser
from .yaml import YamlParser

__all__ = ['detection_formats']


detection_formats = {
    'coco': CocoParser,
    'pickle': PickleParser,
    'yaml': YamlParser
}
