# RCAIDE/Unmanned_Aerial_Vehicle.py
# # 
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.UAV.compute_operating_empty_weight import  compute_operating_empty_weight

# ---------------------------------------------------------------------------------------------------------------------- 
#  UAV_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class Unmanned_Aerial_Vehicle(Vehicle):
    '''Unmanned_Aerial Vehicle Class
    
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
        self.tag  =  'UAV'
        

    def operating_empty_weight(self): 
        """ Compute Operating Empty Weight of UAV Aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self)  
                
        return outputs           
        
        
    
     