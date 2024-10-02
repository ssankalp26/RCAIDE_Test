# RCAIDE/Library/Attributes/Propellants/Butaanol.py
#  
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Propanol Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Butanol(Propellant):
    """Butanol class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            Density at 20C 1 atm
        
        Source: 
    
        """    
        self.tag                       = 'Butanol'
        self.reactant                  = 'O2'
        self.density                   = 809.56                            # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 3.61e7                            # J/kg
        self.energy_density            = 2.92e10                           # J/m^3
        self.lower_heating_value       = 3.44e7                            # J/kg