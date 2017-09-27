#
#   Copyright EAVISE
#

from .vatic import VaticAnnotation
from .dollar import DollarAnnotation
from .darknet import DarknetAnnotation

__all__ = ["formats"]


formats = {
    "dollar": DollarAnnotation,
    "vatic": VaticAnnotation,
    "darknet": DarknetAnnotation
}
