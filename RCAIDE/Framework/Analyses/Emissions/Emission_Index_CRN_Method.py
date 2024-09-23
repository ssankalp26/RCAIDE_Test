## @ingroup Analyses-Emissions
# RCAIDE/Framework/Analyses/Emissions/Emission_Index_CRN_Method.py
# 
# 
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core import  Data 
from RCAIDE.Framework.Analyses    import Process 
from RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method import evaluate_CRN_EI_surrogate ,  build_CRN_EI_surrogates, train_CRN_EI_surrogates
from .Emissions            import Emissions 
  
import numpy as  np

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Emissions
class Emission_Index_CRN_Method(Emissions): 
    """ Emissions Index Chemical Reactor Network Method
    """    
    
    def __defaults__(self): 
        """This sets the default values and methods for the analysis.
    
            Assumptions:
            None
    
            Source:
            None 
            """

        # conditions table, used for surrogate model training
        self.training                   = Data()
        self.training.pressure          = np.linspace(5,30, 10) *1E5
        self.training.temperature       = np.linspace(600, 1000, 10) 
        self.training.air_mass_flowrate = np.linspace(1E-3, 1E2, 10) 
        self.training.fuel_to_air_ratio = np.linspace(0.01, 0.1, 10)
        
        # surrogoate models                 
        self.surrogates                  = Data()  
        
        return

    def initialize(self):     

        # Train surrogate  
        train_CRN_EI_surrogates(self)

        # build surrogate
        build_CRN_EI_surrogates(self)  
     
        return 
        
            
    def evaluate_emissions(self,segment):
        """The default evaluate function. 
        results  
        """      
        # unpack  
        evaluate_CRN_EI_surrogate(self, segment)  
        return
