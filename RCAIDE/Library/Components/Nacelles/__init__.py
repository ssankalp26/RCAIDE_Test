# RCAIDE/Library/Components/Nacelles/__init__.py
# 
"""
=============================================
Nacelles (:mod:`RCAIDE.Library.Components.Nacelles`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Nacelles

Provides functionality for modeling and analyzing aircraft engine nacelles and pylons.

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Nacelle                -- Base class for nacelle implementations
   Body_of_Revolution_Nacelle -- Component for nacelles with body of revolution
   Segment                 -- Component for nacelle segments
   Stack_Nacelle           -- Component for nacelles with stacked engines

Notes
-----
The Nacelles module provides components for different types of engine
housing and mounting systems. This includes traditional turbofan nacelles and
specialized housings for electric propulsion systems.

See Also
--------
RCAIDE.Library.Components.Airframe
RCAIDE.Library.Components.Wings
RCAIDE.Library.Components.Energy.Networks
"""
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Nacelle                    import Nacelle
from .Segment                    import Segment
from .Stack_Nacelle              import Stack_Nacelle
from .Body_of_Revolution_Nacelle import Body_of_Revolution_Nacelle