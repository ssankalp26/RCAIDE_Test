# RCAIDE/Library/Components/Energy/Distributors/__init__.py

"""
=============================================
Distributors (:mod:`RCAIDE.Library.Components.Energy.Distributors`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Energy.Distributors

Provides functionality for modeling and analyzing energy distribution systems in aircraft.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Electrical_Bus    -- Component for electrical power distribution
   Fuel_Line        -- Component for fuel distribution
   Coolant_Line     -- Component for coolant distribution

Notes
-----
The Distributors module contains components for managing various types of energy
distribution systems in aircraft, including electrical, fuel, and cooling systems.
It serves to connect various energycomponents.

See Also
--------
RCAIDE.Library.Components.Energy.Sources
RCAIDE.Library.Components.Energy.Modulators
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .Electrical_Bus                       import Electrical_Bus
from .Fuel_Line                            import Fuel_Line
from .Coolant_Line                         import Coolant_Line

