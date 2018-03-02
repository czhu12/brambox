#
#   Copyright EAVISE
#

import logging

__all__ = ['set_log_level', 'logger']


# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(logging.Formatter('%(levelname)s|%(name)s  %(message)s'))
set_log_level = ch.setLevel

# Logger
logger = logging.getLogger('brambox')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
