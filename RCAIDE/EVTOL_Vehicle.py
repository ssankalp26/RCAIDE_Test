# RCAIDE/EVTOL_Vehicle.py
#  
# Created:  Sep 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Vehicle import Vehicle   
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric.compute_operating_empty_weight import compute_operating_empty_weight

# ---------------------------------------------------------------------------------------------------------------------- 
#  EVTOL_Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class EVTOL_Vehicle(Vehicle):
    '''EVTOL Vehicle Class
    
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
        self.tag  =  'eVTOL'
        

    def operating_empty_weight(self, settings=None): 
        """ Compute Operating Empty Weight of eVTOL Aircraft 
        
            Assumptions:
                None
    
            Source:
                None
        """          
        outputs = compute_operating_empty_weight(self, settings)  
                
        return outputs           
        
        
    
