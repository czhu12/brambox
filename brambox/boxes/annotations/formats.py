#
#   Copyright EAVISE
#

from .cvc import CvcParser
from .darknet import DarknetParser
from .dollar import DollarParser
from .pascalvoc import PascalVOCParser
from .pickle import PickleParser
from .vatic import VaticParser
from .yaml import YamlParser

__all__ = ['annotation_formats']


annotation_formats = {
    'cvc': CvcParser,
    'darknet': DarknetParser,
    'dollar': DollarParser,
    'pickle': PickleParser,
    'pascalvoc': PascalVOCParser,
    'vatic': VaticParser,
    'yaml': YamlParser,
}
