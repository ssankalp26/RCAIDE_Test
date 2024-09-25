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
from RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method import * 
from RCAIDE.Framework.Analyses.Emissions            import Emissions 
  
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
        #self.training.temperature       = np.linspace(600, 1000, 10) 
        #self.training.air_mass_flowrate = np.linspace(1E-3, 1E2, 10) 
        #self.training.fuel_to_air_ratio = np.linspace(0.01, 0.1, 10)
        self.training.temperature       = np.linspace(600, 1000, 3) 
        self.training.air_mass_flowrate = np.linspace(1E-3, 1E2, 3) 
        self.training.fuel_to_air_ratio = np.linspace(0.01, 0.1, 3)        
        
        # surrogoate models                 
        self.surrogates                  = Data() 

        # build the evaluation process
        compute                         = Process()  
        compute.emissions               = None  
        self.process.compute            = compute        
        
        return
    
    def initialize(self):  
        use_surrogate   = self.settings.use_surrogate  

        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            train_CRN_EI_surrogates(self)

            # build surrogate
            build_CRN_EI_surrogates(self)  

        # build the evaluation process
        compute   =  self.process.compute                  
        if use_surrogate == True: 
            compute.emissions  = evaluate_CRN_emission_indices_surrogate
        else:
            compute.emissions  = evaluate_CRN_emission_indices_no_surrogate
        return 


    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.geometry
        """          
        settings = self.settings
        geometry = self.geometry
        results  = self.process.compute(state,settings,geometry)

        return results