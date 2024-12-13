# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Lithium_Air.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module import Generic_Battery_Module  

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Air
# ----------------------------------------------------------------------------------------------------------------------  
class Lithium_Air(Generic_Battery_Module):
    """
    A class for modeling lithium-air battery cells in aircraft energy systems.
    Inherits from the Generic_Battery_Module class.

    Attributes
    ----------
    cell : Data
        Collection of cell-specific properties
        - specific_energy : float
            Energy density of the cell, defaults to 2000 Wh/kg
        - specific_power : float
            Power density of the cell, defaults to 0.66 kW/kg
        - mass_gain_factor : float
            Rate of mass gain per energy unit, defaults to 1.92E-4 kg/Wh

    Notes
    -----
    The Lithium_Air class models lithium-air battery cells, which are characterized
    by very high theoretical energy density. These batteries consume oxygen from
    the air during discharge and gain mass during operation due to the formation
    of lithium oxide.
    
    **Definitions**
    'Specific Energy'
        Energy stored per unit mass of the battery, notably high for Li-air
    'Specific Power'
        Power output capability per unit mass
    'Mass Gain Factor'
        Rate at which the battery gains mass during discharge due to oxygen consumption
    """
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """      
        self.cell.specific_energy  = 2000.     *Units.Wh/Units.kg    # convert to Joules/kg
        self.cell.specific_power   = 0.66      *Units.kW/Units.kg    # convert to W/kg
        self.cell.mass_gain_factor = (1.92E-4) /Units.Wh