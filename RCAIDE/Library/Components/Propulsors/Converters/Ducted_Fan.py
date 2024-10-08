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
        
        self.tag                               = 'ducted_fan'  
        self.number_of_radial_stations         = 20
        self.number_of_rotor_blades            = 12  
        self.tip_radius                        = 1.0
        self.hub_radius                        = 0.1
        self.blade_clearance                   = 0.01
        self.length                            = 1
        self.rotor                             = Data()
        self.stator                            = Data()
        self.rotor.percent_x_location          = 0.4
        self.stator.percent_x_location         = 0.7
        self.cruise                            = Data()
        self.cruise.design_thrust              = None
        self.cruise.design_altitude            = None
        self.cruise.design_angular_velocity    = None
        self.cruise.design_freestream_velocity = None
        self.cruise.design_reference_velocity  = None 
        self.duct_airfoil                      = Data()
        self.hub_geometry                      = Data()
    
    def append_duct_airfoil(self,airfoil):
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
        self.duct_airfoil.append(airfoil)

        return
    

    def append_hub_geometry(self,airfoil):
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
        self.hub_geometry.append(airfoil)

        return                