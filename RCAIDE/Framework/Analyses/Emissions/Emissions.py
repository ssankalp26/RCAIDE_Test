## @ingroup Analyses-Energy
# RCAIDE/Framework/Analyses/Emissions/Emissions.py
# 
# 
# Created:  Jul 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
from RCAIDE.Framework.Analyses import Analysis 

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Emissions
class Emissions(Analysis):
    """ RCAIDE.Framework.Analyses.Emissions.Emissions()
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
            
                    Assumptions:
                    None
            
                    Source:
                    N/A
            
                    Inputs:
                    None
            
                    Outputs:
                    None
            
                    Properties Used:
                    N/A
                """        
        self.tag                   = 'emissions'
        self.compute_emission_flag = True
        
    def evaluate_emissions(self,state):
        
        """Evaluate the emissions produced by the energy network.
    
                Assumptions:
                Network has an "evaluate_emissions" method.
    
                Source:
                N/A
    
                Inputs:
                State data container
    
                Outputs:
                Results of the emissions evaluation method.
    
                Properties Used:
                N/A                
        """
                
        results  = networks.evaluate_thrust(state) 
        
        return results