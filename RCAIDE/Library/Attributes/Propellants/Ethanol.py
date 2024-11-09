# RCAIDE/Library/Attributes/Propellants/Ethanol.py
#  
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Ethanol Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Ethanol(Propellant):
    """Ethanol class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            Density at 15C, 1 atm
        
        Source: 
    
        """    
        self.tag                       = 'Ethanol'
        self.reactant                  = 'O2'
        self.density                   = 793.67                           # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 2.68e7                           # J/kg
        self.energy_density            = 2.13e10                          # J/m^3
        self.lower_heating_value       = 2.67e7                           # J/kg  
        
        # self.fuel_surrogate_chemical_properties    = {'CH3CH2OH':1.0}
        # self.air_chemical_properties               = {'O2':0.2095, 'N2':0.7809, 'AR':0.0096}