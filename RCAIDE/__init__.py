# RCAIDE/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from . import Framework
from . import Library

from .Vehicle  import Vehicle
from .load     import load 
from .save     import save
from .version  import version as __version__
from warnings  import simplefilter
simplefilter('ignore')
