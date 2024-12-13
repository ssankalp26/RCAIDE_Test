# RCAIDE/Compoments/Nacelles/Body_of_Revolution_Nacelle.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data 
from RCAIDE.Library.Components.Airfoils import Airfoil 
from .Nacelle import Nacelle
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ---------------------------------------------------------------------------------------------------------------------- 
class Body_of_Revolution_Nacelle(Nacelle):
    """
    A class for modeling axisymmetric nacelles in aircraft propulsion systems.
    Inherits from the Nacelle class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'body_of_revolution_nacelle'
    Airfoil : Data()
        Data object containing airfoil data
        
    Notes
    -----
    The Body_of_Revolution_Nacelle class models axisymmetric nacelles using
    analytical methods.
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
        
        self.tag                       = 'body_of_revolution_nacelle' 
        self.Airfoil                   = Data()
    
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