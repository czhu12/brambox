#
#   Copyright EAVISE
#

from .pascalvoc import PascalVOCAnnotation
from .vatic import VaticAnnotation
from .dollar import DollarAnnotation

__all__ = ["formats"]


formats = {
    "dollar": DollarAnnotation,
    "vatic": VaticAnnotation,
    "pascalvoc": PascalVOCAnnotation
}
