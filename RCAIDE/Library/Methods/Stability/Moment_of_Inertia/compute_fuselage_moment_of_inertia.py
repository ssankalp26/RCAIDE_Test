# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_wing_moment_of_inertia.py 
# 
# Created:  Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE
from RCAIDE.Framework.Core import Units 

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Wing Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_fuselage_moment_of_inertia(fuselage,center_of_gravity): 
    fuse_weight = fuselage.mass # Edit this call
    I_total = np.zeros((3, 3))
    outer_radius = fuselage.effective_diameter / 2
    inner_radius = 0.75 * fuselage.effective_diameter / 2 # Assume the inner radius is 75 % of the outer radius    
    center_length = fuselage.lengths.total - fuselage.lengths.nose - fuselage.lengths.tail     # Length of the cylinder (found by subtracting the tail adn nose lengths from the total length)
    volume_fraction = Volume_Fraction(outer_radius, inner_radius, center_length, fuselage.lengths.tail) # [hemisphere, cylinder, cone]
    
    # ----------------------------------------------------------------------------------------------------------------------   
    ## Hemisphere
    # ----------------------------------------------------------------------------------------------------------------------   
    origin_hemisphere =  np.array([fuselage.lengths.nose, 0, 0]) + np.array(fuselage.origin)
    m =  fuse_weight * volume_fraction[0] # mass_of_component_hemi
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    I[0][0] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3) # Ixx
    I[1][1] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3)# Iyy
    I[2][2] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3) # Izz

    # global system
    s = np.array(origin_hemisphere) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    I_total = np.array(I_total) + np.array(I_global)
    
    
    # ----------------------------------------------------------------------------------------------------------------------   
    ## cylinder
    # ----------------------------------------------------------------------------------------------------------------------   
    
    m = fuse_weight *volume_fraction[1] #mass_of_component_cylinder
    origin_cylinder =  np.array([fuselage.lengths.nose + h / 2,0, 0]) + np.array(fuselage.origin) # origin of the cylinder is located a the middle of the cylinder
    
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    I[0][0] =  m / 2 *  (outer_radius ** 2 + inner_radius ** 2) # Ixx
    I[1][1] =  m / 12 * (3 * (outer_radius ** 2 + inner_radius ** 2) + center_length ** 2) # Iyy
    I[2][2] =  m / 12 * (3 * (outer_radius ** 2 + inner_radius ** 2) + center_length ** 2) # Izz
    
    # transform moment of inertia to global system
    s = np.array(origin_cylinder) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    I_total = np.array(I_total) + np.array(I_global)

    # ----------------------------------------------------------------------------------------------------------------------   
    ## cone
    # ----------------------------------------------------------------------------------------------------------------------   
    
    h = fuselage.lengths.tail # length of the cone is defined to be the tail length.
    m = fuse_weight *volume_fraction[2] #mass_of_component_cone
    origin_cone =  np.array([fuselage.lengths.total - h,0, 0]) + np.array(fuselage.origin)
    
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    rho = (m / (1 / 3 * np.pi * (outer_radius ** 2 * h - inner_radius ** 2 * (h * inner_radius / outer_radius)))) # density of the cone. Mass divided by volume.
    I[0][0] =  rho * (1 / 3 * np.pi * outer_radius ** 2 * h ** 3 + np.pi / 20 * outer_radius ** 4 *h - 1 / 3 * np.pi * inner_radius ** 2 * (h * inner_radius / outer_radius) ** 3 + np.pi / 20 * inner_radius ** 4 *(h * inner_radius / outer_radius))
    I[1][1] =  rho * (1 / 3 * np.pi * outer_radius ** 2 * h ** 3 + np.pi / 20 * outer_radius ** 4 *h - 1 / 3 * np.pi * inner_radius ** 2 * (h * inner_radius / outer_radius) ** 3 + np.pi / 20 * inner_radius ** 4 *(h * inner_radius / outer_radius))
    I[2][2] =  rho * (np.pi /10 *outer_radius **4 *h -np.pi /10 *inner_radius **4 *(h * inner_radius / outer_radius)) # Izz
    
    # transform moment of inertia to global system
    
    s = np.array(origin_cone) - np.array(center_of_gravity) # vector from the cone base to the center of gravity of the aircraft. 
    I_global =  np.array(I) + m * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - s*np.transpose(s))
    
    I_total = np.array(I_total) + np.array(I_global)
    
    return I_total

def Volume_Fraction(outer_radius, inner_radius, center_length, tail_length):
    
    # Calculate the volume fraction of each of the three components that make up the entire fuselage
    
    volume_cone = np.pi * outer_radius ** 2 * tail_length / 3 - np.pi * inner_radius ** 2 * (tail_length * inner_radius / outer_radius) / 3
    volume_hemisphere = 2 / 3 * np.pi * outer_radius ** 3 -2 / 3 * np.pi * inner_radius ** 3 
    volume_cylinder = np.pi * center_length * (outer_radius ** 2 - inner_radius ** 2)
    
    total_volume = volume_cone + volume_hemisphere + volume_cylinder
    
    fraction = np.array([volume_hemisphere / total_volume, volume_cylinder / total_volume, volume_cone / total_volume])
    
    return fraction

if __name__ == '__main__': 
    main()