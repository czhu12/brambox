#
#   Copyright EAVISE
#

from .pascalvoc import PascalVOCAnnotation
from .vatic import VaticAnnotation
from .dollar import DollarAnnotation
from .darknet import DarknetAnnotation

__all__ = ["formats"]


formats = {
    "darknet": DarknetAnnotation,
    "dollar": DollarAnnotation,
    "vatic": VaticAnnotation,
    "pascalvoc": PascalVOCAnnotation
}
