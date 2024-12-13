# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Aluminum_Air.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module    import Generic_Battery_Module

# ----------------------------------------------------------------------------------------------------------------------
#  Aluminum_Air
# ----------------------------------------------------------------------------------------------------------------------   
class Aluminum_Air(Generic_Battery_Module):
    """
    A class for modeling aluminum-air battery cells in aircraft energy systems.
    Inherits from the Generic_Battery_Module class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'Aluminum Air'
    
    cell : Data
        Collection of cell-specific properties
        - specific_energy : float
            Energy density of the cell, defaults to 1300 Wh/kg
        - specific_power : float
            Power density of the cell, defaults to 0.2 kW/kg
        - water_mass_gain_factor : float
            Rate of water mass gain per energy unit, defaults to 0.000123913 kg/Wh
        - aluminum_mass_factor : float
            Rate of aluminum consumption per energy unit, defaults to 0.000123828 kg/Wh
        - ragone : Data
            Ragone plot characteristics
            - const_1 : float
                First Ragone constant, defaults to 0.8439 kW/kg
            - const_2 : float
                Second Ragone constant, defaults to -4.8647e-004/(Wh/kg)
            - lower_bound : float
                Lower energy density bound, defaults to 1100 Wh/kg
            - upper_bound : float
                Upper energy density bound, defaults to 1600 Wh/kg
    
    mass_gain_factor : float
        Overall mass gain factor, defaults to 0.000110145 kg/Wh

    Notes
    -----
    The Aluminum_Air class models aluminum-air battery cells, which are unique in that
    they consume aluminum and gain mass during operation due to the reaction with oxygen
    and water. These batteries are characterized by high energy density but require
    management of reactant consumption and product accumulation.
    
    **Definitions**
    'Specific Energy'
        Energy stored per unit mass of the battery
    'Specific Power'
        Power output capability per unit mass
    'Ragone Plot'
        Graph showing the relationship between specific power and specific energy
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """
        self.tag                         = 'Aluminum Air'
        self.cell.specific_energy        = 1300.*Units.Wh/Units.kg    # convert to Joules/kg
        self.cell.specific_power         = 0.2*Units.kW/Units.kg      # convert to W/kg
        self.mass_gain_factor            = 0.000110145*Units.kg/Units.Wh
        self.cell.water_mass_gain_factor = 0.000123913*Units.kg/Units.Wh
        self.cell.aluminum_mass_factor   = 0.000123828*Units.kg/Units.Wh # aluminum consumed per energy
        self.cell.ragone.const_1         = 0.8439*Units.kW/Units.kg
        self.cell.ragone.const_2         = -4.8647e-004/(Units.Wh/Units.kg)
        self.cell.ragone.lower_bound     = 1100.*Units.Wh/Units.kg
        self.cell.ragone.upper_bound     = 1600.*Units.Wh/Units.kg