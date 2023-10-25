# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.download_trace import download_trace
from ambient_download.cut_data import cut_traces_into_windows
from ambient_download.save_streamv2 import save_stream
import obspy
import time

def main():
    
    starttime = "2022-06-06T00:00:00.000"
    
    stream = obspy.core.stream.Stream()
    
    """
    for day in tqdm(range(days)):
        int_start_time = start_day + (day*86400)
        current_stream = download_trace(client="IRIS",
                                        network="IU",
                                        station="ANMO",
                                        location="00",
                                        channel="BHZ",
                                        starttime=int_start_time,
                                        timewindow = 86400)
        stream.append(current_stream[0])
    """
    
    test_time = time.perf_counter()
    
    stream = download_trace(client="IRIS",
                           network="IU",
                           station="TUC",
                           location="00",
                           channel="BHZ",
                           starttime=starttime,
                           timewindow = 86400)
    
    print(f'Successfully downloaded data in {time.perf_counter() - test_time} seconds')
    
    cut_stream = cut_traces_into_windows(trace=stream[0],windowlength=3600)
    
    sort_method_list = ['station','year','julday']
    
    save_stream(stream=cut_stream,main_folder='../../Downloaded_Traces',
                sort_method=sort_method_list, adding_data=True)
    print('Successfully saved traces')
    cut_stream.clear()
    
if __name__ == '__main__':
    main()
    