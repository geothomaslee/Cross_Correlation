# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:53:27 2023

@author: tlee4
"""

from correlation import prep_files as prep
from correlation import cross_correlate_ambient_noise as corr
import matplotlib.pyplot as plt
import time

station1_files, station2_files = prep.find_station_files('ANMO', 'TUC', './Downloaded_Traces')

df1, df2 = prep.get_info_from_file_name(station1_files, station2_files, name_structure=None)

pairs_list = prep.create_corresponding_files_list(df1, df2)

"""
xcorr, xcorr_times, xcorr_meta = corr.cross_correlate_ambient_noise(test_pair)
plt.plot(xcorr_times, xcorr)
plt.title('Unaveraged')
plt.show()

xcorr_averaged, xcorr_averaged_times = corr.running_average_filter(xcorr, xcorr_times)
plt.plot(xcorr_averaged_times,xcorr_averaged)
plt.title('Averaged')
plt.show()
"""

start_time = time.perf_counter()

xcorr_list, xcorr_times = corr.multi_correlate(pairs_list,time_method='seconds')
xcorr_stack = corr.xcorr_stack(xcorr_list)
plt.plot(xcorr_times,xcorr_stack)
plt.title('Unaveraged')
plt.show()

end_time = time.perf_counter()

print(f'Correlation took {end_time - start_time} seconds')

xcorr_averaged, xcorr_averaged_times = corr.running_average_filter(xcorr_stack,xcorr_times,avg_window=20)
plt.plot(xcorr_averaged_times, xcorr_averaged,'r-')
plt.title('Averaged')
plt.show()


xcorr_averaged_times_cut = xcorr_averaged_times[3540:3660]
xcorr_averaged_cut = xcorr_averaged[3540:3660]
plt.plot(xcorr_averaged_times_cut,xcorr_averaged_cut)
plt.title('Averged Zoomed')
plt.show()

xcorr_times_cut = xcorr_times[3540:3660]
xcorr_cut = xcorr_stack[3540:3660]
plt.plot(xcorr_times_cut,xcorr_cut,'g-')
plt.title('Unaveraged Zoomed')
plt.show()


    





