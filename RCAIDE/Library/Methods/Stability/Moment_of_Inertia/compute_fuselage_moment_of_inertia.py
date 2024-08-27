# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_wing_moment_of_inertia.py 
# 
# Created:  Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE 

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Wing Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------  
def compute_fuselage_moment_of_inertia(fuselage,center_of_gravity): 
    # ADD CODE
    I_total = np.zeros((3, 3))

    ## Hemisphere
    
    origin_hemisphere =  np.array([fuselage.lengths.nose, 0, 0]) + np.array(fuselage.origin)
    m = mass_of_component_hemi
    I =  np.zeros((3, 3))
    outer_radius = fuselage.effective_diameter / 2
    inner_radius = 0.75 * fuselage.effective_diameter / 2 # Assume the inner radius is 75 % of the outer radius
    
    # Moment of inertia in local system
    I[0][0] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3) # Ixx
    I[1][1] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3)# Iyy
    I[2][2] =  2 * m / 5 *  (outer_radius ** 5 - inner_radius ** 5) /(outer_radius **3 -inner_radius **3) # Izz

    # global system
    s = np.array(origin_hemisphere) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * np.array(np.dot(s, s)) * np.array(np.identity(3)) - np.array(np.dot(s, np.transpose(s)))
    I_total = np.array(I_total) + np.array(I_global)
    
    ## cylinder
    
    h = fuselage.lengths.total - fuselage.lengths.nose - fuselage.lengths.tail
    m = mass_of_component_cylinder
    origin_cylinder =  np.array([fuselage.lengths.nose + h / 2,0, 0]) + np.array(fuselage.origin) # origin of the cylinder is located a tthe middle of the cylinder
    
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    I[0][0] =  m / 2 *  (outer_radius ** 2 + inner_radius ** 2) # Ixx
    I[1][1] =  m / 12 * (3 * (outer_radius ** 2 + inner_radius ** 2) + h ** 2) # Iyy
    I[2][2] =  m / 12 * (3 * (outer_radius ** 2 + inner_radius ** 2) + h ** 2) # Izz
    
    # transform moment of inertia to global system
    s = np.array(origin_cylinder) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * np.array(np.dot(s, s)) * np.array(np.identity(3)) - np.array(np.dot(s, np.transpose(s)))
    I_total = np.array(I_total) + np.array(I_global)

    ## cone
    
    h = fuselage.lengths.tail
    m = mass_of_component_cone
    origin_cone =  np.array([fuselage.lengths.total - h,0, 0]) + np.array(fuselage.origin)
    
    I =  np.zeros((3, 3))
    
    # Moment of inertia in local system
    rho = (m / (1 / 3 * np.pi * (outer_radius ** 2 * h - inner_radius ** 2 * (h * inner_radius / outer_radius))))
    I[0][0] =  rho * (1 / 3 * np.pi * outer_radius ** 2 * h ** 3 + np.pi / 20 * outer_radius ** 4 *h - 1 / 3 * np.pi * inner_radius ** 2 * (h * inner_radius / outer_radius) ** 3 + np.pi / 20 * inner_radius ** 4 *(h * inner_radius / outer_radius))
    I[1][1] =  rho * (1 / 3 * np.pi * outer_radius ** 2 * h ** 3 + np.pi / 20 * outer_radius ** 4 *h - 1 / 3 * np.pi * inner_radius ** 2 * (h * inner_radius / outer_radius) ** 3 + np.pi / 20 * inner_radius ** 4 *(h * inner_radius / outer_radius))
    I[2][2] =  rho * (np.pi /10 *outer_radius **4 *h -np.pi /10 *inner_radius **4 *(h * inner_radius / outer_radius)) # Izz
    
    # transform moment of inertia to global system
    
    s = np.array(origin_cone) - np.array(center_of_gravity)
    
    I_global = np.array(I) + m * np.array(np.dot(s, s)) * np.array(np.identity(3)) - np.array(np.dot(s, np.transpose(s)))
    I_total = np.array(I_total) + np.array(I_global)
    

    return I_total 