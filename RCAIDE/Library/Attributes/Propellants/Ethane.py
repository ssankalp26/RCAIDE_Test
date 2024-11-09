# RCAIDE/Library/Attributes/Propellants/Ethane.py
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
class Ethane(Propellant):
    """Ethane class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            Density at -90C, 1 atm
        
        Source: 
    
        """    
        self.tag                       = 'Ethane'
        self.reactant                  = 'O2'
        self.density                   = 545.6                            # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 5.19e7                           # J/kg
        self.energy_density            = 2.83e10                          # J/m^3
        self.lower_heating_value       = 4.75e7                           # J/kg  
        
        # self.fuel_surrogate_chemical_properties    = {'C2H6':1.0}
        #self.air_chemical_properties               = {'O2':0.2095, 'N2':0.7809, 'AR':0.0096}