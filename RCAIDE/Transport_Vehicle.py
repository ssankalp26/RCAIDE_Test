# RCAIDE/Transport_Vehicle.py
# # 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.Common.compute_operating_empty_weight import  compute_operating_empty_weight
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  UAV_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class Transport_Vehicle(Vehicle):
    '''Transport Vehicle Class
    
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
        self.tag  =  'Transport'
        

    def operating_empty_weight(self, settings=None, method_type='RCAIDE'): 
        """ Compute Operating Empty Weight of transport Aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self, settings, method_type)
                
        return outputs     