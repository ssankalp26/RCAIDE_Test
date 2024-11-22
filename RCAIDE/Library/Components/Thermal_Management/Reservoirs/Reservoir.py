# RCAIDE/Library/Compoments/Thermal_Management/Reservoirs/Reservoir.py
# 
# 
# Created:  Mar 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Library.Components                                                      import Component 
from RCAIDE.Library.Attributes.Coolants.Glycol_Water                                import Glycol_Water
from RCAIDE.Library.Attributes.Materials.Polyetherimide                             import Polyetherimide
from RCAIDE.Library.Methods.Thermal_Management.Reservoirs.Reservoir_Tank            import compute_mixing_temperature, append_reservoir_conditions, append_reservoir_segment_conditions
from RCAIDE.Library.Plots.Thermal_Management.plot_reservoir_conditions              import plot_reservoir_conditions

# ----------------------------------------------------------------------
#  Reservoir
# ----------------------------------------------------------------------
## @ingroup Attributes-Coolants
class Reservoir(Component):
    """Holds values for a coolant reservoir

    Assumptions:
    None
    
    Source:
    None
    """

    def __init__(self):
        """This sets the default values.

        Assumptions:
        None

        Source:
        Values commonly available  
        """
        self.tag                          = 'coolant_reservoir'
        self.material                     = Polyetherimide()
        self.coolant                      = Glycol_Water()
        self._length                      = 0.3          # [m]
        self._width                       = 0.3          # [m]
        self._height                      = 0.3          # [m]
        self.thickness                    = 5e-3         # [m] 
        # Update mass properties after initializing dimensions and coolant
        self.update_mass_properties()

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value
        self.update_mass_properties()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.update_mass_properties()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.update_mass_properties()

    @property
    def coolant(self):
        return self._coolant

    @coolant.setter
    def coolant(self, value):
        self._coolant = value
        self.update_mass_properties()

    @property
    def surface_area(self):
        """Calculate surface area dynamically."""
        return 2 * (
            self._length * self._width +
            self._width * self._height +
            self._length * self._height
        )  # [m^2]
    
    @property
    def volume(self):
        """Calculate volume dynamically."""
        return self._length * self._width * self._height  # [m^3]

    @property
    def mass(self):
        """Calculate and return mass dynamically."""
        return self.coolant.density * self.volume  # [kg]

    def update_mass_properties(self):
        """Automatically update the stored mass."""
        self.mass_properties.mass = self.mass

    def append_operating_conditions(self,segment,coolant_line,add_additional_network_equation = False):
        append_reservoir_conditions(self,segment,coolant_line,add_additional_network_equation)
        return
    
    def append_segment_conditions(self,segment,coolant_line,conditions):
        append_reservoir_segment_conditions(self,segment,coolant_line,conditions)
        return    

    def compute_reservior_coolant_temperature(self,state,coolant_line,delta_t,t_idx):
        compute_mixing_temperature(self,state,coolant_line,delta_t,t_idx)
        return
    
    def plot_operating_conditions(self,results, coolant_line,save_filename, save_figure,show_legend,file_type,width, height):
        plot_reservoir_conditions(self, results, coolant_line,save_filename,save_figure,show_legend,file_type,width, height)
        return    
