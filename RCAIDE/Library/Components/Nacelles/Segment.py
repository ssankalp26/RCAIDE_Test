# RCAIDE/Library/Compoments/Nacelles/Segment.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ---------------------------------------------------------------------------------------------------------------------- 
class Segment(Component):
    """
    A class for modeling nacelle segments in aircraft propulsion system design.
    Inherits from the Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'segment'
    
    height : float
        Height of the segment in meters, defaults to 0.0
    
    width : float
        Width of the segment in meters, defaults to 0.0

    percent_x_location : float
        Location of segment as percentage of total nacelle length, defaults to 0.0
    
    percent_y_location : float
        Location of segment as percentage of total nacelle width, defaults to 0.0
    
    percent_z_location : float
        Location of segment as percentage of total nacelle height, defaults to 0.0
    
    curvature : float
        Curvature of the segment, defaults to 2 (super ellipse)
    
    Notes
    -----
    The Segment class models individual sections of a nacelle, allowing for
    detailed geometric definition of the nacelle shape. Each segment can have
    unique dimensions and properties, enabling the creation of complex nacelle
    geometries through multiple segment combinations.
    
    **Definitions**
    'Wetted Area'
        Total surface area exposed to airflow
    'Flow Symmetry'
        Indicates if flow conditions are identical on both sides
    'Percent X Location'
        Position along nacelle length as percentage from front
    """
    
    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

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
        self.tag                      = 'segment' 
        self.orientation_euler_angles = [0.,0.,0.]  
        self.percent_x_location       = 0  
        self.percent_y_location       = 0
        self.percent_z_location       = 0 
        self.height                   = 0 
        self.width                    = 0 
        self.curvature                = 2 # super ellipse 
        
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