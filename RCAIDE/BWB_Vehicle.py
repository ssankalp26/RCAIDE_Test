# RCAIDE/BWB_Vehicle.py
# # 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.BWB.compute_operating_empty_weight import  compute_operating_empty_weight
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  BWB_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class BWB_Vehicle(Vehicle):
    '''BWB Vehicle Class
    
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
        self.tag  =  'BWB'
        

    def operating_empty_weight(self): 
        """ Compute Operating Empty Weight of BWB Aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self)
                
        return outputs     