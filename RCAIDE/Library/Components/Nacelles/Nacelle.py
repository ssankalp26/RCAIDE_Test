# RCAIDE/Compoments/Nacelles/Nacelle.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data 
from RCAIDE.Library.Components          import Component  
from RCAIDE.Library.Components.Airfoils import Airfoil
import scipy as sp
import numpy as np
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ---------------------------------------------------------------------------------------------------------------------- 
class Nacelle(Component):
    """
    A base class for modeling aircraft engine nacelles and their integration.
    Inherits from the Component class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'nacelle'
    origin : array
        Origin of the nacelle [x, y, z], defaults to [0.0, 0.0, 0.0]
    aerodynamic_center : array
        Aerodynamic center of the nacelle [x, y, z], defaults to [0.0, 0.0, 0.0]
    areas : Data
        Collection of area-related properties
        - wetted : float
            Total wetted area, defaults to 0.0
        - frontal : float
            Frontal area, defaults to 0.0
        - inlet : float
            Inlet area, defaults to 0.0
        - exit : float
            Exit area, defaults to 0.0

    mass_properties : Data
        Collection of mass-related properties
        - mass : float
            Total mass of the nacelle assembly, defaults to 0.0
        - center_of_gravity : array
            CG location of the nacelle [x, y, z], defaults to [0.0, 0.0, 0.0]
        - moments_of_inertia : array
            Moments of inertia [Ixx, Iyy, Izz], defaults to [0.0, 0.0, 0.0]
    diameter : float
        Diameter of the nacelle, defaults to 0.0
    inlet_diameter : float
        Diameter of the inlet, defaults to 0.0
    length : float
        Length of the nacelle, defaults to 0.0
    orientation_euler_angles : array
        Euler angles [roll, pitch, yaw], defaults to [0.0, 0.0, 0.0]
    flow_through : bool
        Whether the nacelle is flow-through, defaults to True
    has_pylon : bool
        Whether the nacelle has a pylon, defaults to True
    differential_pressure : float
        Differential pressure across the nacelle, defaults to 0.0
    cowling_airfoil_angle : float
        Angle of the cowling airfoil, defaults to 0.0

    Methods
    -------
    nac_vel_to_body()
        Rotates from the systems body frame to the nacelles velocity frame
    body_to_nac_vel()
        Rotates from the systems body frame to the nacelles velocity frame
    vec_to_vel()
        Rotates from the nacelles vehicle frame to the nacelles velocity frame

    Notes
    -----
    The Nacelle class serves as a base class for all nacelle types,
    providing common attributes and methods for nacelle modeling. It includes
    properties needed for aerodynamic, structural, and integration analysis.
    This class is meant to be inherited by specific nacelle implementations.
    
    **Definitions**
    'Wetted Area'
        Total surface area exposed to airflow
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
        """      
        
        self.tag                       = 'nacelle'
        self.origin                    = [[0.0,0.0,0.0]]
        self.aerodynamic_center        = [0.0,0.0,0.0]  
        self.areas                     = Data()
        self.areas.front_projected     = 0.0
        self.areas.side_projected      = 0.0
        self.areas.wetted              = 0.0 
        self.diameter                  = 0.0 
        self.inlet_diameter            = 0.0
        self.length                    = 0.0   
        self.orientation_euler_angles  = [0.,0.,0.]    
        self.flow_through              = True
        self.has_pylon                 = True
        self.differential_pressure     = 0.0    
        self.cowling_airfoil_angle     = 0.0

    def append_operating_conditions(self,segment,fuel_line,propulsor): 
        return

    def nac_vel_to_body(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """
        
        body2nacvel = self.body_to_nac_vel()
        
        r = sp.spatial.transform.Rotation.from_matrix(body2nacvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat
    
    def body_to_nac_vel(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None 
        """
        
        # Go from body to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        # Go from vehicle frame to nacelle vehicle frame: rot 1 including the extra body rotation
        rots    = np.array(self.orientation_euler_angles) * 1. 
        vehicle_2_nac_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()        
        
        # GO from the nacelle vehicle frame to the nacelle velocity frame: rot 2
        nac_vec_2_nac_vel = self.vec_to_vel()
        
        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_nac_vec)
        rot_mat = np.matmul(rot1,nac_vec_2_nac_vel) 
        return rot_mat    
    
    

    def vec_to_vel(self):
        """This rotates from the nacelles vehicle frame to the nacelles velocity frame

        Assumptions:
        There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        
        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        return rot_mat
    
    
        