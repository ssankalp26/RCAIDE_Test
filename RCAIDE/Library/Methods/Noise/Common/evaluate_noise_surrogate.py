def  compute_noise_surrogate():
    
        
        
        # Step 1: compute noise at hemishere locations
        compute_rotor_noise(distributor,propulsor,segment,settings)
        conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_dBA
        conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_1_3_spectrum
        
        phi_data = settings.noise_hemisphere_phi_angle_bounds     
        theta_data = settings.noise_hemisphere_theta_angle_bounds   

        # Step 2: create surrogate here
        surrogates = Data()
        surrogates.SPL_dBA       = RegularGridInterpolator((phi_data , theta_data),training.Clift_alpha        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.SPL_spectra        = RegularGridInterpolator((phi_data, theta_data),training.Clift_beta         ,method = 'linear',   bounds_error=False, fill_value=None) 
        
        
        #total_SPL_dBA[:,None,:]
        #total_SPL_spectra[:,None,:,:]
        
        # Step 3: query surrogate 
        
        # Step 4: store data 
        
        #total_SPL_dBA     = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_dBA[:,None,:]),axis =1),sum_axis=1)
        #total_SPL_spectra = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,:],conditions.noise[distributor.tag][propulsor.tag][sub_item.tag].SPL_1_3_spectrum[:,None,:,:]),axis =1),sum_axis=1) 
         
                                      
        conditions.noise.total_SPL_dBA              = total_SPL_dBA
        conditions.noise.total_SPL_1_3_spectrum_dBA = total_SPL_spectra
        
        return
    
