# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Lithium_Sulfur.py
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# package imports
from RCAIDE.Framework.Core import Units
from .Generic_Battery_Module import Generic_Battery_Module

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Sulfur
# ---------------------------------------------------------------------------------------------------------------------- 
class Lithium_Sulfur(Generic_Battery_Module):
    """
    Lithium-Sulphur battery.
    A class for modeling lithium-sulfur battery cells in aircraft energy systems.
    Inherits from the Generic_Battery_Module class.

    Attributes
    ----------
    cell : Data
        Collection of cell-specific properties
        - specific_energy : float
            Energy density of the cell, defaults to 500 Wh/kg
        - specific_power : float
            Power density of the cell, defaults to 1 kW/kg
        - ragone : Data
            Ragone plot characteristics
            - const_1 : float
                First Ragone constant, defaults to 245.848 kW/kg
            - const_2 : float
                Second Ragone constant, defaults to -0.00478 /(Wh/kg)
            - lower_bound : float
                Lower energy density bound, defaults to 300 Wh/kg
            - upper_bound : float
                Upper energy density bound, defaults to 700 Wh/kg

    Notes
    -----
    The Lithium_Sulfur class models lithium-sulfur battery cells, which are known
    for their high theoretical energy density. These batteries use sulfur as the
    cathode material and metallic lithium as the anode material, offering potential
    advantages in terms of cost and energy density compared to traditional
    lithium-ion batteries.
    
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
        self.cell.specific_energy    = 500     *Units.Wh/Units.kg
        self.cell.specific_power     = 1       *Units.kW/Units.kg
        self.cell.ragone.const_1     = 245.848 *Units.kW/Units.kg
        self.cell.ragone.const_2     = -.00478 /(Units.Wh/Units.kg)
        self.cell.ragone.lower_bound = 300     *Units.Wh/Units.kg
        self.cell.ragone.upper_bound = 700     *Units.Wh/Units.kg