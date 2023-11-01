# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:53:27 2023

@author: tlee4
"""

from correlation import prep_files as prep
from correlation import cross_correlate_ambient_noise as corr
import matplotlib.pyplot as plt
from statistics import mode
import numpy as np

station1_files, station2_files = prep.find_station_files('ANMO', 'TUC', '~/Documents/Correlation_Testing_Data')

df1, df2 = prep.get_info_from_file_name(station1_files, station2_files, name_structure=None)

pairs_list = prep.create_corresponding_files_list(df1, df2)

#test_pair = [pairs_list[0][0],pairs_list[0][1]]
#xcorr_times, xcorr, xcorr_meta = corr.cross_correlate_ambient_noise(test_pair,low=0.05)

x_corr_list = []

for pair in pairs_list:
    xcorr_times, xcorr, xcorr_meta = corr.cross_correlate_ambient_noise(pair, low=0.05)
    x_corr_list.append(xcorr)
    
len_list = []
for i, xcorr in enumerate(x_corr_list):
    len_list.append(len(xcorr))
    
npts_expected = mode(len_list)
print(f'Mode: {npts_expected}')

for i, xcorr in enumerate(x_corr_list):
    print(len(xcorr))
    if len(xcorr) == npts_expected:
        pass
    else:
        xcorr_new = xcorr.copy()
        add_pts = npts_expected - len(xcorr)
        print(f'Adding {add_pts} points!')
        for add in range(add_pts):
            xcorr_new = np.append(xcorr_new, 0)
        
        print(xcorr_new[-1])
            
        x_corr_list[i] = xcorr_new
 
len_list = []
for i, xcorr in enumerate(x_corr_list):
    len_list.append(len(xcorr))
    

x_corr_stack = sum(x_corr_list) / len(x_corr_list)

plt.plot(xcorr_times,x_corr_stack)
    
    



    





