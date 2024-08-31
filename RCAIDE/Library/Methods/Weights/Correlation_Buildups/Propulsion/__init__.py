## @defgroup Methods-Weights-Correlations-Propulsion Propulsion
# RCAIDE/Methods/Weights/Correlations/Propulsion/__init__.py
# 

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from .compute_jet_engine_weight                             import compute_jet_engine_weight
from .compute_piston_engine_weight                          import compute_piston_engine_weight 
from .integrated_propulsion                                 import integrated_propulsion
from .integrated_propulsion_general_aviation                import integrated_propulsion_general_aviation
from .compute_motor_weight                                  import compute_motor_weight
from Legacy.trunk.S.Methods.Weights.Dynamo_Supply.dynamo_supply_mass_estimation   import dynamo_supply_mass_estimation