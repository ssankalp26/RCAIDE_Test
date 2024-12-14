# RCAIDE/Library/__init__.py 
"""
=============================================
Library (:mod:`Library`)
=============================================

.. currentmodule:: Library

Core library containing all analysis modules, components, and methods for RCAIDE

Sub-folders
============================================

.. autosummary::
   :toctree: generated/

   Attributes    -- Vehicle and analysis attributes
   Components    -- Physical component definitions and models
   Methods       -- Analysis and calculation methods
   Mission       -- Mission profile and segment definitions
   Plots        -- Visualization and plotting utilities

Notes
-----
The Library module serves as the main container for all RCAIDE functionality,
organizing the code into logical categories for vehicle definition, analysis,
and visualization.
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from . import Attributes
from . import Components 
from . import Methods 
from . import Mission
from . import Plots 