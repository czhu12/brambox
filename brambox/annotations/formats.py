#
#   Copyright EAVISE
#

from .vatic import VaticAnnotation
from .dollar import DollarAnnotation

__all__ = ["formats"]


formats = {
    "dollar": DollarAnnotation,
    "vatic": VaticAnnotation
}
