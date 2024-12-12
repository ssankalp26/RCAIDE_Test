# RCAIDE/Library/Attributes/Propellants/Methane.py
#  
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant 

# ---------------------------------------------------------------------------------------------------------------------- 
# Methane Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Methane(Propellant):
    """Methane class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            Density at -162C, 1 atm
        
        Source:  
        """    
        self.tag                       = 'Methane'
        self.reactant                  = 'O2'
        self.density                   = 422.6                            # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 5.34e7                           # J/kg
        self.energy_density            = 2.26e10                          # J/m^3
        self.lower_heating_value       = 5.0e7                            # J/kg  
        

        self.use_high_fidelity_kinetics_model      =  False 
        self.fuel_surrogate_chemical_properties    = {'CH4':1.0}
        self.fuel_chemical_properties              = {'CH4':1.0}      # [2] More accurate kinetic mechanism, slower simulation    
        self.air_chemical_properties               = {'O2':0.2095, 'N2':0.7809, 'AR':0.0096}
        self.surrogate_species_list                = ['CO', 'CO2', 'H2O']
        self.species_list                          = ['CO', 'CO2', 'H2O', 'NO', 'NO2', 'CSOLID']   
        self.surrogate_chemical_kinetics           = 'Fuel_Surrogate.yaml'
        self.chemical_kinetics                     = 'Fuel.yaml'
        self.oxidizer                              = 'Air.yaml'        
        
        self.global_warming_potential_100.CO2       = 1     # CO2e/kg  
        self.global_warming_potential_100.H2O       = 0.06  # CO2e/kg  
        self.global_warming_potential_100.SO2       = -226  # CO2e/kg  
        self.global_warming_potential_100.NOx       = 52    # CO2e/kg  
        self.global_warming_potential_100.Soot      = 1166  # CO2e/kg    
        self.global_warming_potential_100.Contrails = 11    # kg/CO2e/km          