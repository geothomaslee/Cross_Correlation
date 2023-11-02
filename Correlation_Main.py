# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:53:27 2023

@author: tlee4
"""

from correlation import prep_files as prep
from correlation import cross_correlate_ambient_noise as corr
import matplotlib.pyplot as plt
from obspy.signal.filter import bandpass

station1_files, station2_files = prep.find_station_files('ANMO', 'TUC', './Downloaded_Traces')

df1, df2 = prep.get_info_from_file_name(station1_files, station2_files, name_structure=None)

pairs_list = prep.create_corresponding_files_list(df1, df2)

"""
test_pair = pairs_list[0]
xcorr, xcorr_times, xcorr_meta = corr.cross_correlate_ambient_noise(test_pair, low=0.01, high=5)
plt.plot(xcorr_times, xcorr)
plt.show()

xcorr, xcorr_times, xcorr_meta = corr.cross_correlate_ambient_noise(test_pair, low=0.01, high=10)
plt.plot(xcorr_times, xcorr)
plt.show()
"""

xcorr_list, xcorr_times = corr.multi_correlate(pairs_list,low=0.01,high=5)

xcorr_stack = corr.xcorr_stack(xcorr_list)

xcorr_stack_bp = bandpass(xcorr_stack,freqmin=0.01,freqmax=5,df=20)

plt.plot(xcorr_times,xcorr_stack_bp)

    



    





