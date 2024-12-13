# RCAIDE/Library/Components/Fuselages/Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core                import Data 
from RCAIDE.Library.Components.Component  import Container
from RCAIDE.Library.Components            import Component
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia import  compute_fuselage_moment_of_inertia

 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
class Fuselage(Component):
    """
    A standard fuselage class for tube and wing aircraft configurations that handles geometry, 
    segmentation, and fuel tank definitions.

    Attributes
    ----------
    tag : str
        Identifier for the fuselage component
        
    origin : list
        Origin point of the fuselage in [x, y, z] coordinates
        
    aerodynamic_center : list
        Location of the aerodynamic center in [x, y, z] coordinates
        
    differential_pressure : float
        Pressure differential between inside and outside of fuselage
        
    seats_abreast : float
        Number of seats side by side in the fuselage
        
    seat_pitch : float
        Distance between seats front to back
        
    number_coach_seats : float
        Total number of coach class seats
        
    areas : Data
        Collection of fuselage area measurements
        - front_projected : float
            Front view projected area
        - side_projected : float
            Side view projected area
        - wetted : float
            Total wetted area of the fuselage
            
    effective_diameter : float
        Effective diameter of the fuselage
        
    width : float
        Width of the fuselage
        
    heights : Data
        Collection of height measurements at various fuselage stations
        - maximum : float
            Maximum height of the fuselage
        - at_quarter_length : float
            Height at 25% of fuselage length
        - at_three_quarters_length : float
            Height at 75% of fuselage length
        - at_wing_root_quarter_chord : float
            Height at wing root quarter chord
        - at_vertical_root_quarter_chord : float
            Height at vertical tail root quarter chord
            
    lengths : Data
        Collection of length measurements
        - nose : float
            Length of nose section
        - tail : float
            Length of tail section
        - total : float
            Total length of fuselage
        - cabin : float
            Length of cabin section
        - fore_space : float
            Length of space forward of cabin
        - aft_space : float
            Length of space aft of cabin
            
    x_rotation : float
        Rotation angle around x-axis
        
    y_rotation : float
        Rotation angle around y-axis
        
    z_rotation : float
        Rotation angle around z-axis
        
    fineness : Data
        Fineness ratios
        - nose : float
            Nose fineness ratio
        - tail : float
            Tail fineness ratio
            
    nose_curvature : float
        Curvature parameter for nose section
        
    tail_curvature : float
        Curvature parameter for tail section
        
    fuel_tanks : Container
        Container for fuel tank definitions
        
    vsp_data : Data
        OpenVSP specific geometry data
        - xsec_surf_id : str
            Surface ID for cross-sections
        - xsec_num : int
            Number of cross-sections
            
    Segments : Container
        Container for fuselage segment definitions

    Methods
    -------
    append_segment(segment)
        Adds a new segment to the fuselage
        
    append_fuel_tank(fuel_tank)
        Adds a new fuel tank to the fuselage
        
    compute_moment_of_inertia(center_of_gravity)
        Computes the moment of inertia of the fuselage

    Notes
    -----
    The fuselage class is designed for conventional tube and wing aircraft configurations.
    It provides a comprehensive framework for defining the geometry and characteristics
    of an aircraft fuselage including its segments, fuel tanks, and various measurements.
    
    **Definitions**
    'Fineness Ratio'
        The ratio of length to maximum diameter of a body
    'Wetted Area'
        The total surface area of the fuselage that is in contact with the airflow
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
        
        self.tag                                    = 'fuselage'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0] 
        self.differential_pressure                  = 0.0    
        self.seats_abreast                          = 0.0
        self.seat_pitch                             = 0.0
        self.number_coach_seats                     = 0.0

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
        
        self.lengths                                = Data()     
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0 
        self.lengths.cabin                          = 0.0 
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0 
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0 

        self.fineness                               = Data() 
        self.fineness.nose                          = 0.0 
        self.fineness.tail                          = 0.0  
        self.nose_curvature                         = 1.5
        self.tail_curvature                         = 1.5   
    
        self.fuel_tanks                             = Container()
 
        self.vsp_data                               = Data()
        self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        self.vsp_data.xsec_num                      = None  # Number if XSecs in fuselage geom. 
        self.Segments                               = Container()
        
    def append_segment(self,segment):
        """ Adds a segment to the fuselage. 
    
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
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return
    
    def append_fuel_tank(self,fuel_tank):
        """ Adds a fuel tank to the fuselage 
    
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
        if not isinstance(fuel_tank,Data):
            raise Exception('input component must be of type Data()')
    
        # Store data
        self.Fuel_Tanks.append(fuel_tank)

        return 

    def compute_moment_of_inertia(self, center_of_gravity=[[0, 0, 0]]): 
        I =  compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I    