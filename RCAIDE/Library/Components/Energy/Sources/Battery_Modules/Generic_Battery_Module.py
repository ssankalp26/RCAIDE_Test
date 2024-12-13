# RCAIDE/Library/Components/Energy/Sources/Battery_Modules/Generic_Battery_Module.py
# 
# Created:  Mar 2024, M. Clarke
# Modified: Sep 2024, S. Shekar
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
from RCAIDE.Framework.Core        import Data
from RCAIDE.Library.Components    import Component   
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Common.append_battery_conditions import append_battery_conditions, append_battery_segment_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Battery
# ----------------------------------------------------------------------------------------------------------------------     
class Generic_Battery_Module(Component):
    """
    A base class for modeling battery modules in aircraft energy systems.
    Inherits from the Component class.

    Attributes
    ----------
    energy_density : float
        Energy density of the battery module, defaults to 0.0
    
    current_energy : float
        Current energy stored in the battery, defaults to 0.0
    
    current_capacitor_charge : float
        Current charge level of the capacitor, defaults to 0.0
    
    capacity : float
        Total energy capacity of the battery, defaults to 0.0
    
    length : float
        Physical length of the battery module, defaults to 0.0
    
    width : float
        Physical width of the battery module, defaults to 0.0
    
    height : float
        Physical height of the battery module, defaults to 0.0
    
    volume_packaging_factor : float
        Factor accounting for packaging volume, defaults to 1.05
    
    BMS_additional_weight_factor : float
        Factor for battery management system weight, defaults to 1.42
    
    orientation_euler_angles : list
        Vector of angles defining default orientation, defaults to [0.,0.,0.]
    
    cell : Data
        Collection of cell-specific properties
        - chemistry : None
            Type of battery chemistry
        - discharge_performance_map : None
            Map of discharge performance characteristics
        - ragone : Data
            Ragone plot characteristics
            - const_1 : float
                First Ragone constant, defaults to 0.0
            - const_2 : float
                Second Ragone constant, defaults to 0.0
            - lower_bound : float
                Lower energy density bound, defaults to 0.0
            - i : float
                Current value, defaults to 0.0
    
    electrical_configuration : Data
        Battery electrical configuration
        - series : int
            Number of cells in series, defaults to 1
        - parallel : int
            Number of cells in parallel, defaults to 1
    
    geometrtic_configuration : Data
        Battery geometric configuration
        - normal_count : int
            Count in normal direction, defaults to 1
        - parallel_count : int
            Count in parallel direction, defaults to 1
        - normal_spacing : float
            Spacing in normal direction, defaults to 0.02
        - stacking_rows : int
            Number of stacking rows, defaults to 3
        - parallel_spacing : float
            Spacing in parallel direction, defaults to 0.02

    Methods
    -------
    append_operating_conditions(segment, bus)
        Appends operating conditions for a flight segment and bus
    
    append_battery_segment_conditions(bus, conditions, segment)
        Appends battery-specific conditions for a segment

    Notes
    -----
    The Generic_Battery_Module class serves as a base class for all battery types,
    providing common attributes and methods for battery modeling. It includes
    physical, electrical, and geometric configurations necessary for detailed
    battery system modeling.
    
    **Definitions**
    'BMS'
        Battery Management System - controls and monitors battery operation
    'Ragone Plot'
        Graph showing relationship between specific power and specific energy
    'Volume Packaging Factor'
        Factor accounting for additional volume needed for battery packaging
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """
      
       
        self.energy_density                                    = 0.0
        self.current_energy                                    = 0.0
        self.current_capacitor_charge                          = 0.0
        self.capacity                                          = 0.0
            
        self.length                                            = 0.0
        self.width                                             = 0.0
        self.height                                            = 0.0
        self.volume_packaging_factor                           = 1.05
        self.BMS_additional_weight_factor                      = 1.42
                 
        self.orientation_euler_angles                          = [0.,0.,0.]  # vector of angles defining default orientation of rotor        
                     
        self.cell                                              = Data()
        self.cell.chemistry                                    = None                             
        self.cell.discharge_performance_map                    = None  
        self.cell.ragone                                       = Data()
        self.cell.ragone.const_1                               = 0.0     # used for ragone functions; 
        self.cell.ragone.const_2                               = 0.0     # specific_power=ragone_const_1*10^(specific_energy*ragone_const_2)
        self.cell.ragone.lower_bound                           = 0.0     # lower bound specific energy for which ragone curves no longer make sense
        self.cell.ragone.i                                     = 0.0 
 
        self.electrical_configuration                          = Data()
        self.electrical_configuration.series                   = 1
        self.electrical_configuration.parallel                 = 1   
        
        self.geometrtic_configuration                          = Data() 
        self.geometrtic_configuration.normal_count             = 1
        self.geometrtic_configuration.parallel_count           = 1
        self.geometrtic_configuration.normal_spacing           = 0.02
        self.geometrtic_configuration.stacking_rows            = 3
        self.geometrtic_configuration.parallel_spacing         = 0.02                
 
    def append_operating_conditions(self,segment,bus):  
        append_battery_conditions(self,segment,bus)  
        return
    
    def append_battery_segment_conditions(self,bus, conditions, segment):
        append_battery_segment_conditions(self,bus, conditions, segment)
        return