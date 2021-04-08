"""
Frites
======

Network, Connectivity and Hierarchically Organized Structures
"""
import logging

from netchos import io

__version__ = "0.0.0"

# -----------------------------------------------------------------------------
# Set 'info' as the default logging level
logger = logging.getLogger('netchos')
io.set_log_level('info')
