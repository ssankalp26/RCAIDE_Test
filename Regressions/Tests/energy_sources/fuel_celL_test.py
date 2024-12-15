# Regression/scripts/network_isolated_battery_cell/cell_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Core   import Units, Data   
from RCAIDE.Library.Plots    import * 

# package imports  
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

# local imports 
import sys 
import os
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Fuel_Cell   import vehicle_setup , configs_setup  

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main():   
    
    # Operating conditions for battery p
    marker_size           = 5 
    V_ul_true             = np.array([3.176391931635407,3.1422615279089]) 

    # PLot parameters 
    marker                = ['s' ,'o' ,'P']
    linestyles            = ['-','--',':']
    linecolors            = cm.inferno(np.linspace(0.2,0.8,3))     
    plt.rcParams.update({'font.size': 12})
    fig1 = plt.figure('Cell Test') 
    fig1.set_size_inches(12,7)   
    axes1  = fig1.add_subplot(3,2,1)
    axes2  = fig1.add_subplot(3,2,2)  
    axes3  = fig1.add_subplot(3,2,3) 
    axes4  = fig1.add_subplot(3,2,4) 
    axes5  = fig1.add_subplot(3,2,5) 
    axes6  = fig1.add_subplot(3,2,6)  
 

    fuel_cell_model     = ['lithium_ion_nmc','lithium_ion_lfp']      
    for i in range(len(fuel_cell_model)):
        
        vehicle  = vehicle_setup(fuel_cell_model[i]) 
        
        # Set up vehicle configs
        configs  = configs_setup(vehicle)
    
        # create analyses
        analyses = analyses_setup(configs)
    
        # mission analyses
        mission  = mission_setup(analyses,vehicle) 
        
        # create mission instances (for multiple types of missions)
        missions = missions_setup(mission) 
         
        # mission analysis 
        results = missions.base_mission.evaluate()  
        
        # Voltage Cell Regression
        V_ul        = results.segments[0].conditions.energy.bus.battery_modules[fuel_cell_model[i]].cell.voltage_under_load[2][0]   
        print('Under load voltage: ' + str(V_ul))
        V_ul_diff   = np.abs(V_ul - V_ul_true[i])
        print('Under load voltage difference')
        print(V_ul_diff) 
        assert np.abs((V_ul_diff)/V_ul_true[i]) < 1e-6
        
        for segment in results.segments.values(): 
            volts         = segment.conditions.energy.bus.voltage_under_load[:,0] 
            SOC           = segment.conditions.energy.bus.battery_modules[fuel_cell_model[i]].cell.state_of_charge[:,0]   
            cell_temp     = segment.conditions.energy.bus.battery_modules[fuel_cell_model[i]].cell.temperature[:,0]   
            Amp_Hrs       = segment.conditions.energy.bus.battery_modules[fuel_cell_model[i]].cell.charge_throughput[:,0]                   
              
            if fuel_cell_model[i] == 'PEM':
                axes1.plot(Amp_Hrs , volts , marker= marker[i], linestyle = linestyles[i],  color= linecolors[j]  , markersize=marker_size   ,label = fuel_cell_model[i] ) 
                axes3.plot(Amp_Hrs , SOC   , marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j], markersize=marker_size   ,label = fuel_cell_model[i]) 
                axes5.plot(Amp_Hrs , cell_temp, marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size,label = fuel_cell_model[i])              
            else:
                axes2.plot(Amp_Hrs , volts , marker= marker[i], linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size   ,label = fuel_cell_model[i] ) 
                axes4.plot(Amp_Hrs , SOC   , marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j], markersize=marker_size   ,label = fuel_cell_model[i] ) 
                axes6.plot(Amp_Hrs , cell_temp, marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size,label = fuel_cell_model[i] )              
             
    legend_font_size = 6                     
    axes1.set_ylabel('Voltage $(V_{UL}$)')  
    axes1.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes1.set_ylim([2.5,5]) 
    axes1.set_xlim([0,7])
    axes2.set_xlabel('Amp-Hours (A-hr)') 
    axes2.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes2.set_ylim([2.5,5])   
    axes2.set_xlim([0,7])   
    axes3.set_ylabel('SOC')  
    axes3.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes3.set_ylim([0,1]) 
    axes3.set_xlim([0,7]) 
    axes4.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes4.set_ylim([0,1])   
    axes4.set_xlim([0,7])       
 
    return  
 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):    
    #   Initialize the Analyses     
    analyses = RCAIDE.Framework.Analyses.Vehicle()  
    
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)
 
    #  Planet Analysis
    planet  = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)
 
    #  Atmosphere Analysis
    atmosphere                 = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses     

def mission_setup(analyses,vehicle):
 
    #   Initialize the Mission 
    mission            = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag        = 'fuel_cell_cycle_test'   
    Segments           = RCAIDE.Framework.Mission.Segments 
    base_segment       = Segments.Segment()    

    # Charge Segment 
    segment                                 = Segments.Ground.Battery_Recharge(base_segment)      
    segment.analyses.extend(analyses.charge) 
    segment.cutoff_SOC                      = 1.0  
    segment.initial_battery_state_of_charge = 0.2  
    segment.tag                             = 'Recharge' 
    mission.append_segment(segment)   

         
    segment                                 = Segments.Ground.Battery_Discharge(base_segment) 
    segment.analyses.extend(analyses.discharge)  
    segment.tag                             = 'Discharge_1' 
    segment.time                            = 100
    segment.initial_battery_state_of_charge = 1  
    mission.append_segment(segment)
    
    segment                                = Segments.Ground.Battery_Discharge(base_segment) 
    segment.tag                            = 'Discharge_2'
    segment.analyses.extend(analyses.discharge)   
    segment.time                           = 100
    mission.append_segment(segment)        
    
    return mission 

def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  
 
if __name__ == '__main__':
    main()
    plt.show()