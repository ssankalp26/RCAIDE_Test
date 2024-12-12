# RCAIDE/Energy/Networks/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Components.Energy.Networks import Battery_Ducted_Fan                           as legacy_battery_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Ducted_Fan                                   as legacy_ducted_fan 
from Legacy.trunk.S.Components.Energy.Networks import Liquid_Rocket                                as legacy_liquid_rocket
from Legacy.trunk.S.Components.Energy.Networks import Propulsor_Surrogate                          as legacy_propulsor_surrogate
from Legacy.trunk.S.Components.Energy.Networks import PyCycle                                      as legacy_pycycle
from Legacy.trunk.S.Components.Energy.Networks import Ramjet                                       as legacy_ramjet
from Legacy.trunk.S.Components.Energy.Networks import Scramjet                                     as legacy_scramjet
from Legacy.trunk.S.Components.Energy.Networks import Serial_Hybrid_Ducted_Fan                     as legacy_serial_hybrid_ducted_fan 
from Legacy.trunk.S.Components.Energy.Networks import Turboelectric_HTS_Ducted_Fan                 as legacy_turboelectric_hts_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Turboelectric_HTS_Dynamo_Ducted_Fan          as legacy_turboelectric_hts_dynamo_ducted_fan
from Legacy.trunk.S.Components.Energy.Networks import Turbojet_Super                               as legacy_turbojet
 
from .Network       import Network
from .Fuel          import Fuel
from .Electric      import Electric
from .Solar         import Solar
from .Human_Powered import Human_Powered