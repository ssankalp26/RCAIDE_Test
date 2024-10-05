# RCAIDE/Compoments/Propulsors/Converters/Ducted_Fan.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data  
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Ducted_Fan(Data):
    """ This is a ducted fan component
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """      
        
        self.tag                       = 'ducted_fan' 
        self.design_thrust              = None
        self.design_altitude            = None
        self.design_angular_velocity    = None
        self.number_of_blades           = 10
        self.number_of_radial_stations  = 20
        self.design_freestream_velocity = None
        self.design_reference_velocity  = None
        self.Airfoil                    = Data()
    
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment 
    
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

        # Assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Airfoil.append(airfoil)

        return            