# RCAIDE/Library/Components/Fuselages/__init__.py
# 

"""
=============================================
Fuselages (:mod:`Fuselages`)
=============================================

.. currentmodule:: Fuselages

A module containing classes and methods for modeling aircraft fuselages, including
standard tube fuselages and blended wing body configurations.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Segment                    -- Class for defining individual fuselage segments
   Fuselage                   -- Base class for all fuselage types
   Blended_Wing_Body_Fuselage -- Class for modeling blended wing body fuselages
   Tube_Fuselage             -- Class for modeling conventional tube fuselages

Notes
-----
This module provides a comprehensive framework for defining and analyzing different
types of aircraft fuselages. It includes support for both conventional tube-and-wing
configurations and more advanced designs like blended wing bodies.

See Also
--------
RCAIDE.Library.Components
"""

from .Segment                    import Segment
from .Fuselage                   import Fuselage
from .Blended_Wing_Body_Fuselage import Blended_Wing_Body_Fuselage 
from .Tube_Fuselage              import Tube_Fuselage