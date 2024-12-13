# RCAIDE/Components/Costs/__init__.py
# 
"""
=============================================
Costs (:mod:`RCAIDE.Library.Components.Costs`)
=============================================

.. currentmodule:: RCAIDE.Library.Components.Costs

Provides functionality for analyzing and calculating various costs associated with aircraft components.

Functions
==========================================

.. autosummary::
   :toctree: generated/

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Industrial_Costs    -- Class for calculating industrial and manufacturing costs
   Operating_Costs     -- Class for calculating operational costs

Notes
-----
The Costs module provides tools for estimating and analyzing different types of costs
associated with aircraft components, including both industrial (manufacturing) and operational expenses.

See Also
--------
RCAIDE.Library.Components
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Components.Costs.Costs import Industrial_Costs, Operating_Costs