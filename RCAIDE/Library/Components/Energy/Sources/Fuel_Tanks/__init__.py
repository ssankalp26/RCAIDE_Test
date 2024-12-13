# RCAIDE/Library/Components/Energy/Sources/Fuel_Tanks/__init__.py
# 
"""
=============================================
Fuel_Tanks (:mod:`RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks

Provides functionality for modeling and analyzing various types of fuel tanks in aircraft systems.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Fuel_Tank           -- Base class for fuel tank implementations
   Central_Fuel_Tank   -- Component for central/fuselage fuel tanks
   Wing_Fuel_Tank      -- Component for wing-integrated fuel tanks

Notes
-----
The Fuel_Tanks module provides components for different types of fuel storage
systems used in aircraft. This includes central fuel tanks typically located
in the fuselage, wing-integrated fuel tanks, and a generic base class for
implementing custom fuel tank configurations.

See Also
--------
RCAIDE.Library.Components.Energy.Sources.Battery_Modules
RCAIDE.Library.Components.Energy.Sources.Solar_Panels
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Fuel_Tank  import Fuel_Tank
from .Central_Fuel_Tank import Central_Fuel_Tank
from .Wing_Fuel_Tank   import  Wing_Fuel_Tank