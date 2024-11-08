# RCAIDE/Library/Attributes/Propellants/Propane.py
#  
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Propane Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Propane(Propellant):
    """Propane class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source: 
        """    
        self.tag                       = 'Propane'
        self.reactant                  = 'O2'
        self.density                   = 584.2                            # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 5.03e7                           # J/kg
        self.energy_density            = 2.94e10                          # J/m^3
        self.lower_heating_value       = 4.6e7                            # J/kg  

 

        #Carbon: 81.71%
#Hydrogen: 18.29%