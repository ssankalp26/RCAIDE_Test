## @ingroup Library-Components-Airfoils
# RCAIDE/Compoments/Airfoils/NACA_4_Series_Airfoil.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Airfoil import Airfoil
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Airfoils 
class NACA_4_Series_Airfoil(Airfoil):
    """
    A class for generating and managing NACA 4-series airfoil profiles. Inherits from the base Airfoil class.

    Attributes
    ----------
    tag : str
        Identifier for the airfoil, defaults to 'NACA_4_Series'
    
    NACA_4_Series_code : str
        Four-digit NACA designation code, defaults to '0012'
        - First digit: Maximum camber in percentage of chord
        - Second digit: Position of maximum camber in tenths of chord
        - Last two digits: Maximum thickness in percentage of chord

    Methods
    -------
    __defaults__()
        Sets the default values for the NACA 4-series airfoil attributes

    Notes
    -----
    The NACA 4-Series airfoil class provides functionality to create and manage
    standard NACA 4-digit series airfoils. These airfoils are defined by a simple
    numerical code that specifies their camber and thickness characteristics.
    
    **Definitions**
    'NACA'
        National Advisory Committee for Aeronautics
    'Camber'
        The curvature of the mean line between upper and lower surfaces
    'Chord'
        The straight line distance from airfoil leading edge to trailing edge
    """
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """        
        self.tag                   = 'NACA_4_Series'
        self.NACA_4_Series_code    = '0012'
        return 
