# RCAIDE/Library/Components/Airfoils/__init__.py
# 
"""
=============================================
Airfoils (:mod:`RCAIDE.Library.Components.Airfoils`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Airfoils

Provides functionality for defining and analyzing airfoil geometries and characteristics.

Functions
==========================================

.. autosummary::
   :toctree: generated/

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Airfoil              -- Base class for airfoil definitions
   NACA_4_Series_Airfoil -- Class for NACA 4-series airfoil generation

Notes
-----
The Airfoils module contains tools for creating and analyzing different types of airfoils,
including standard NACA series and custom airfoil definitions.

See Also
--------
RCAIDE.Library.Components.Wings
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Airfoil               import Airfoil
from .NACA_4_Series_Airfoil import NACA_4_Series_Airfoil