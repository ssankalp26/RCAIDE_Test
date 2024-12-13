# RCAIDE/Library/Compoments/Fuselage/Segment.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Data, Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ----------------------------------------------------------------------------------------------------------------------  
class Segment(Component):
    """
    A class for defining fuselage segments in RCAIDE.

    Attributes
    ----------
    tag : str
        Identifier for the segment, defaults to 'segment'
        
    prev : Segment
        Reference to the previous segment in the fuselage
        
    next : Segment
        Reference to the next segment in the fuselage
        
    percent_x_location : float
        Percentage location along x-axis, defaults to 0
        
    percent_y_location : float
        Percentage location along y-axis, defaults to 0
        
    percent_z_location : float
        Percentage location along z-axis, defaults to 0
        
    height : float
        Height of the segment, defaults to 0
        
    width : float
        Width of the segment, defaults to 0
        
    curvature : float
        Curvature parameter of the segment, defaults to 2

    Notes
    -----
    The Segment class is used to define individual sections of a fuselage.
    Each segment can be connected to form a complete fuselage shape with
    specified dimensions and positions.
    
    **Definitions**
    'Segment'
        A discrete section of the fuselage with defined geometric properties
    'Curvature'
        Parameter that defines how the segment transitions between cross-sections
    """
    def __defaults__(self): 
        self.tag                     = 'segment'
        self.prev                    = None
        self.next                    = None    
        self.percent_x_location      = 0  
        self.percent_y_location      = 0
        self.percent_z_location      = 0 
        self.height                  = 0 
        self.width                   = 0 
        self.curvature               = 2
        
## @ingroup Components-Wings
class Segment_Container(Container):
    """ Container for fuselage segment
    
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

    def get_children(self):
        """ Returns the components that can go inside
        
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
        
        return []