# RCAIDE/Library/Components/__init__.py
"""
=============================================
Components (:mod:`Components`)
=============================================

.. currentmodule:: Components

Module containing all component definitions and models for vehicle analysis

Sub-folders
============================================

.. autosummary::
   :toctree: generated/

   Propulsors           -- Propulsion system components
   Energy               -- Energy system components
   Thermal_Management   -- Thermal management system components
   Airfoils            -- Airfoil definitions and analysis
   Booms               -- Structural boom components
   Configs             -- Vehicle configuration definitions
   Fuselages           -- Fuselage components
   Landing_Gear        -- Landing gear components
   Nacelles            -- Engine nacelle components
   Payloads            -- Payload components
   Systems             -- Vehicle systems components
   Wings               -- Wing components

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Component           -- Base class for all vehicle components
   Network            -- Network class for component connections
   Mass_Properties    -- Class for handling component mass properties

Notes
-----
This module serves as the main container for all physical components that can be used
to build up a complete vehicle model. Each component is designed to be modular and
can be combined through the Network class.
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from .Component        import Component
from . Network         import  Network
from .Mass_Properties  import Mass_Properties
  
from . import Propulsors
from . import Energy
from . import Thermal_Management 
from . import Airfoils
from . import Booms
from . import Configs
from . import Fuselages
from . import Landing_Gear
from . import Nacelles
from . import Payloads
from . import Systems
from . import Wings