# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""
import time

module_load_time = time.perf_counter()

from ambient_download.bulk_seis_download import bulk_download_seismic_data
#from ambient_download.seis_download import download_seismic_data
from ambient_download.get_ambient_times import get_ambient_windows
from ambient_download.save_stream import save_stream_traces

init_time = time.perf_counter()

starttime = "2023-09-27T00:00:00.000"
window_length = 60
total_time =  180

starttimes, endtimes = get_ambient_windows(starttime, window_length, total_time, 1)

download_time = time.perf_counter()

ambient_stream = bulk_download_seismic_data(client="IRIS",
                                            starttime=starttimes,
                                            endtime=endtimes,
                                            network="IU",
                                            station="ANMO",
                                            location="00",
                                            channel="LHZ")

print(ambient_stream)

save_time = time.perf_counter()

save_stream_traces(stream=ambient_stream, sort_method="station",
                   force_overwrite=True)

final_time = time.perf_counter()

print(f'Time to load module: {init_time - module_load_time}')
print(f'Time to initialize: {download_time - init_time}')
print(f'Time to download: {save_time - download_time}')
print(f'Time to save: {final_time - save_time}')
    