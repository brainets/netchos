"""
Netchos
=======

Network, Connectivity and Hierarchically Organized Structures
"""
import logging

from netchos import io, utils  # noqa
from netchos.heatmap import heatmap  # noqa
from netchos.network import network  # noqa
from netchos.circular import circular  # noqa

__version__ = "0.0.0"

# -----------------------------------------------------------------------------
# Set 'info' as the default logging level
logger = logging.getLogger('netchos')
io.set_log_level('info')
