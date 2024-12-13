#RCAIDE/Library/Components/Energy/Modulators/__init__.py
"""
=============================================
Modulators (:mod:`RCAIDE.Library.Components.Energy.Modulators`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Energy.Modulators

Provides functionality for controlling and modulating energy flow in aircraft systems.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Electronic_Speed_Controller    -- Component for controlling electric motor speed
   Fuel_Selector                 -- Component for managing fuel source selection
   Solar_Logic                   -- Component for managing solar power systems
   HTS_DC_Dynamo_Basic          -- Component for high temperature superconducting DC power
   HTS_DC_Supply                -- Component for HTS DC power supply management

Notes
-----
The Modulators module provides components for controlling and managing different types
of energy flows in aircraft systems. This includes electronic speed control for motors,
fuel selection systems, solar power management, and high temperature superconducting
power systems.

See Also
--------
RCAIDE.Library.Components.Energy.Sources
RCAIDE.Library.Components.Energy.Distributors
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .Electronic_Speed_Controller                  import Electronic_Speed_Controller
from .Fuel_Selector                                import Fuel_Selector
from .Solar_Logic                                  import Solar_Logic
from Legacy.trunk.S.Components.Energy.Distributors import HTS_DC_Dynamo_Basic
from Legacy.trunk.S.Components.Energy.Distributors import HTS_DC_Supply 


