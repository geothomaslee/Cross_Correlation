# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.download_trace import download_trace
from ambient_download.cut_data import cut_traces_into_windows
from ambient_download.save_streamv2 import save_stream
from obspy import UTCDateTime
import obspy
import time


def main():
    
    days = 365
    start_day = UTCDateTime("2022-06-06T00:00:00.000")
    
    stream = obspy.core.stream.Stream()
    
    download_start_time = time.perf_counter()
    
    for day in range(days):
        int_start_time = start_day + (day*86400)
        current_stream = download_trace(client="IRIS",
                                        network="IU",
                                        station="ANMO",
                                        location="00",
                                        channel="BHZ",
                                        starttime=int_start_time,
                                        timewindow = 86400)
        stream.append(current_stream[0])
    
    print(f'Successfully downloaded data in {time.perf_counter() - download_start_time} seconds')
    
    cut_start_time = time.perf_counter()
    
    for i, trace in enumerate(stream):
        print(i)
        cut_stream = cut_traces_into_windows(trace=trace,windowlength=3600)
        
        sort_method_list = ['station','year','julday']
        
        save_stream(stream=cut_stream,sort_method=sort_method_list,adding_data=True)
        print('Successfully saved traces')
    
    print(f'Successfully cut and saved data with an average time of {(time.perf_counter() - cut_start_time) / days} seconds per day')
if __name__ == '__main__':
    main()
    