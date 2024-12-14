# RCAIDE/Compoments/Booms/Boom.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
from RCAIDE.Library.Components import Component 
from RCAIDE.Framework.Core     import Data, Container 
 
# ----------------------------------------------------------------------------------------------------------------------
#  BOOM
# ----------------------------------------------------------------------------------------------------------------------  
class Boom(Component):
    """
    A standard boom component for a rotor system.

    Attributes
    ----------
    tag : str
        Identifier for the boom component, defaults to 'boom'
    origin : list
        3D coordinates of the boom origin, default [[0.0,0.0,0.0]]
    aerodynamic_center : list
        3D coordinates of the aerodynamic center, default [0.0,0.0,0.0]
    
    areas : Data
        Collection of area measurements
        - front_projected : float
            Front projected area
        - side_projected : float
            Side projected area
        - wetted : float
            Wetted area of the boom
    
    effective_diameter : float
        Effective diameter of the boom
    width : float
        Width of the boom
    
    heights : Data
        Collection of height measurements
        - maximum : float
            Maximum height of the boom
        - at_quarter_length : float
            Height at 25% of boom length
        - at_three_quarters_length : float
            Height at 75% of boom length
        - at_wing_root_quarter_chord : float
            Height at wing root quarter chord
        - at_vertical_root_quarter_chord : float
            Height at vertical root quarter chord
    
    x_rotation : float
        Rotation angle around x-axis
    y_rotation : float
        Rotation angle around y-axis
    z_rotation : float
        Rotation angle around z-axis
    
    lengths : Data
        Collection of length measurements
        - nose : float
            Length of the nose section
        - total : float
            Total length of the boom
        - cabin : float
            Length of the cabin section
        - fore_space : float
            Length of space in front
        - aft_space : float
            Length of space in rear
    
    fineness : Data
        Fineness ratios
        - nose : float
            Fineness ratio of nose
        - tail : float
            Fineness ratio of tail
    
    differential_pressure : float
        Pressure differential across the boom
    
    vsp_data : Data
        Vehicle Sketch Pad related data
        - xsec_surf_id : str
            VSP cross-section surface identifier
        - xsec_num : int
            Number of cross-sections in rotor boom geometry
    
    Segments : Container
        Container for boom segments

    Methods
    -------
    append_segment(segment)
        Adds a new segment to the boom's Segments container

    Notes
    -----
    The boom component is primarily used in rotor-based aircraft configurations
    and serves as a structural element for mounting rotors and other components.
    
    **Definitions**
    'Fineness Ratio'
        The ratio of length to maximum diameter of a body
    'Wetted Area'
        The total surface area that would be in contact with the flow
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """       
        
        self.tag                                    = 'boom'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0]  
                 
        self.areas                                  = Data()
        self.areas.front_projected                  = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
                         
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0 
                         
        self.heights                                = Data()
        self.heights.maximum                        = 0.0
        self.heights.at_quarter_length              = 0.0
        self.heights.at_three_quarters_length       = 0.0
        self.heights.at_wing_root_quarter_chord     = 0.0
        self.heights.at_vertical_root_quarter_chord = 0.0
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0
             
        self.lengths                                = Data()
        self.lengths.nose                           = 0.0 
        self.lengths.total                          = 0.0
        self.lengths.cabin                          = 0.0
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0
                 
        self.fineness                               = Data()
        self.fineness.nose                          = 0.0
        self.fineness.tail                          = 0.0
             
        self.differential_pressure                  = 0.0 
              
        # For VSP     
        self.vsp_data                               = Data()
        self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        self.vsp_data.xsec_num                      = None  # Number if XSecs in rotor_boom geom.
                        
        self.Segments                               = Container()
        
    def append_segment(self,segment):
        """ Adds a segment to the rotor_boom. 
    
        Assumptions:
            None
            
        Source:
            None
        
        Args:
            self       : boom                  [unitless]
            segment    : cross-section of boom [unitless]   
            
        Outputs:
            None 
        """ 

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment) 
        
        return 

class Container(Component.Container):
    def get_children(self):
        """ Returns the components that can go inside
    
        Assumptions:
            None
            
        Source:
            None
        
        Args:
            self       : container of booms [unitless]    
            
        Outputs:
            Boom       : boom               [unitless] 
        """ 
        return [Boom]

# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------ 
Boom.Container = Container
