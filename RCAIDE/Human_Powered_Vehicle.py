# RCAIDE/Human_Powered_Vehicle.py
# # 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.Human_Powered.compute_operating_empty_weight import  compute_operating_empty_weight
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  Human_Powered_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class Human_Powered_Vehicle(Vehicle):
    '''Human_Powered Vehicle Class
    
    '''
    def __defaults__(self): 
        """This sets the default for main wings in RCAIDE.
    
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
        self.tag  =  'Human_Powered'
        

    def operating_empty_weight(self, settings=None, method_type='RCAIDE'): 
        """ Compute Operating Empty Weight of human powered aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self, settings, method_type)
                
        return outputs     