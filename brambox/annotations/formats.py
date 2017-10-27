#
#   Copyright EAVISE
#

from .cvc import CvcParser
from .darknet import DarknetParser
from .dollar import DollarParser
from .yaml import YamlParser

__all__ = ['formats']


formats = {
    'cvc': CvcParser,
    'darknet': DarknetParser,
    'dollar': DollarParser,
    'yaml': YamlParser
}
