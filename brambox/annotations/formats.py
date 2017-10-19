#
#   Copyright EAVISE
#

from .darknet import DarknetParser
from .yaml import YamlParser

__all__ = ['formats']


formats = {
    'darknet': DarknetParser,
    'yaml': YamlParser
}
