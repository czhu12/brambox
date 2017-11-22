#
#   Copyright EAVISE
#

from .pickle import PickleParser
from .yaml import YamlParser

__all__ = ['detection_formats']


detection_formats = {
    'pickle': PickleParser,
    'yaml': YamlParser,
}
