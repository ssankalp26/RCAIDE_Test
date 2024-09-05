# RCAIDE/General_Aviation_Vehicle.py
# # 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.General_Aviation.compute_operating_empty_weight import  compute_operating_empty_weight
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  General_Aviation_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class General_Aviation_Vehicle(Vehicle):
    '''General_Aviation Vehicle Class
    
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
        self.tag  =  'General_Aviation'
        

    def operating_empty_weight(self): 
        """ Compute Operating Empty Weight of General Aviation Aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self)
                
        return outputs     