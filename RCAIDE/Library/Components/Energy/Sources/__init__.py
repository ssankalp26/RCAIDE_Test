# RCAIDE/Library/Components/Energy/Sources/__init__.py
# 
"""
=============================================
Sources (:mod:`RCAIDE.Library.Components.Energy.Sources`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Energy.Sources

Provides functionality for modeling and analyzing various energy sources in aircraft systems.

Sub-folders
============================================

.. autosummary::
   :toctree: generated/

   Battery_Modules  -- Components for battery-based energy storage
   Fuel_Tanks      -- Components for fuel storage and management
   Solar_Panels    -- Components for solar energy collection

Notes
-----
The Sources module provides components for different types of energy sources
used in aircraft systems. This includes battery modules for electrical energy
storage, fuel tanks for chemical energy storage, and solar panels for renewable
energy collection.

See Also
--------
RCAIDE.Library.Components.Energy.Distributors
RCAIDE.Library.Components.Energy.Modulators
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from . import Battery_Modules
from . import Fuel_Tanks
from . import Solar_Panels