## @ingroup Library-Attributes-Propellants
# RCAIDE/Library/Attributes/Propellants/Liquid_Natural_Gas.py
# 
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant   

# ---------------------------------------------------------------------------------------------------------------------- 
#  Gaseous_Hydrogen Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants 
class Liquid_Natural_Gas(Propellant):
    """Liquid natural gas fuel class,
    """

    def __defaults__(self):
        """This sets the default values. 
    
    Assumptions:
        None
    
    Source:
        None
        """    
        self.tag             = 'Liquid_Natural_Gas'
        self.reactant        = 'O2'
        self.density         = 414.2                            # kg/m^3 
        self.specific_energy = 53.6e6                           # J/kg
        self.energy_density  = 22200.0e6                        # J/m^3
        
        self.use_high_fidelity_kinetics_model      =  True 
        self.fuel_surrogate_chemical_properties    = {'CH4':0.85, 'C2H6':0.1, 'C3H8':0.05}
        
        # volume fractions of dry, gaseous NG: https://www.sciencedirect.com/science/article/pii/S1875510016304139?via%3Dihub
        #self.fuel_chemical_properties = {"CH4":0.96, "C2H6":0.02, "C3H8":0.006,
        #                                 "I-C4H10":0.0018, "N-C4H10":0.0012, "I-C5H12":0.0014, 
        #                                 "N-C5H12":0.0006, "C6H14":0.0010, "C7H16":0.008}
        
        self.fuel_chemical_properties              = {'CH4':0.85, 'C2H6':0.1, 'C3H8':0.05}           
        self.air_chemical_properties               = {'O2':0.2095, 'N2':0.7809, 'AR':0.0096}
        self.surrogate_species_list                = ['CO', 'CO2', 'H2O']
        self.species_list                          = ['CO', 'CO2', 'H2O', 'NO', 'NO2', 'CSOLID']
        self.surrogate_chemical_kinetics           = 'Fuel_Surrogate.yaml'
        self.chemical_kinetics                     = 'Fuel.yaml'
        self.oxidizer                              = 'Air.yaml'        