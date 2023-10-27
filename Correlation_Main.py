# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:53:27 2023

@author: tlee4
"""

from correlation import prep_files as prep
from correlation import cross_correlate_ambient_noise as corr
import matplotlib.pyplot as plt

station1_files, station2_files = prep.find_station_files('ANMO', 'TUC', '~/Documents/Correlation_Testing_Data')

df1, df2 = prep.get_info_from_file_name(station1_files, station2_files, name_structure=None)

pairs_list = prep.create_corresponding_files_list(df1, df2)


test_pair = [pairs_list[0][1],pairs_list[0][1]]
xcorr_times, xcorr = corr.cross_correlate_ambient_noise(test_pair,low=0.05)

plt.plot(xcorr_times, xcorr)





