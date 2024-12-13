# RCAIDE/Components/Landing_Gear/__init__.py
# 
"""
=============================================
Landing_Gear (:mod:`RCAIDE.Library.Components.Landing_Gear`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Landing_Gear

Provides functionality for modeling and analyzing aircraft landing gear systems.

Classes
-------
.. autosummary::
   :toctree: generated/
   Landing_Gear        -- Base class for landing gear implementations
   Nose_Gear          -- Component for nose landing gear
   Main_Gear          -- Component for main landing gear

Notes
-----
The Landing_Gear module provides components for different types of aircraft
landing gear systems. This includes traditional wheeled configurations like
nose and main gear. The module handles gear geometry,
kinematics, and load characteristics.

See Also
--------
RCAIDE.Library.Components.Airframe
RCAIDE.Library.Components.Wings
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Landing_Gear import Landing_Gear
from .Main_Landing_Gear import Main_Landing_Gear
from .Nose_Landing_Gear import Nose_Landing_Gear