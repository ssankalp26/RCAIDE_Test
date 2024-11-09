# RCAIDE/Methods/Energy/Sources/Battery/Lithium_Ion_LFP/update_lfp_cell_age.py
# 
# 
# Created:  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np  
 
# ----------------------------------------------------------------------------------------------------------------------
# update_lfp_cell_age
# ----------------------------------------------------------------------------------------------------------------------  
def update_lfp_cell_age(battery,segment, battery_conditions,increment_battery_age_by_one_day):  
    """ This is an aging model for 18650 lithium-iron-phosphate batteries. 
   
    Source: 
    Liu, Yong, et al. "Degradation mechanism of LiFePO4/graphite batteries: 
    Experimental analyses of calendar aging and cycling aging
      
    Assumptions:
    None
    """
    n_series   = battery.electrical_configuration.series
    SOC        = battery_conditions.cell.state_of_charge
    V_ul       = battery_conditions.voltage_under_load/n_series
    t          = battery_conditions.cell.cycle_in_day         
    Q_prior    = battery_conditions.cell.charge_throughput[-1,0] 
    Temp       = np.mean(battery_conditions.cell.temperature) 
    
    # aging model  
    delta_DOD = abs(SOC[0][0] - SOC[-1][0])
    rms_V_ul  = np.sqrt(np.mean(V_ul**2)) 


    return 
