#
#   Copyright EAVISE
#

from .darknet import DarknetParser
from .dollar import DollarParser
from .yaml import YamlParser

__all__ = ['formats']


formats = {
    'darknet': DarknetParser,
    'dollar': DollarParser,
    'yaml': YamlParser
}
