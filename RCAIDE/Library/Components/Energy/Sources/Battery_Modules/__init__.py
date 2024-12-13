# RCAIDE/Library/Compoments/Energy/Sources/Batteries/__init__.py
# 
"""
=============================================
Battery_Modules (:mod:`RCAIDE.Library.Components.Energy.Sources.Battery_Modules`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Energy.Sources.Battery_Modules

Provides functionality for modeling and analyzing various types of battery modules used in aircraft systems.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Aluminum_Air           -- Component for aluminum-air battery systems
   Generic_Battery_Module -- Base class for battery module implementations
   Lithium_Ion_LFP       -- Component for lithium iron phosphate batteries
   Lithium_Ion_NMC       -- Component for lithium nickel manganese cobalt batteries
   Lithium_Sulfur        -- Component for lithium-sulfur battery systems
   Lithium_Air           -- Component for lithium-air battery systems

Notes
-----
The Battery_Modules module provides components for different types of battery
technologies used in aircraft systems. This includes various lithium-based
batteries, aluminum-air batteries, and a generic battery module base class.

See Also
--------
RCAIDE.Library.Components.Energy.Sources.Fuel_Tanks
RCAIDE.Library.Components.Energy.Sources.Solar_Panels
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Aluminum_Air           import Aluminum_Air
from .Generic_Battery_Module import Generic_Battery_Module
from .Lithium_Ion_LFP        import Lithium_Ion_LFP
from .Lithium_Ion_NMC        import Lithium_Ion_NMC  
from .Lithium_Sulfur         import Lithium_Sulfur
from .Lithium_Air            import Lithium_Air 
