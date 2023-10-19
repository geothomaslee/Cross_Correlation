# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:52 2023

@author: tlee4
"""

from get_ambient_times import get_ambient_windows
from download_trace import download_trace

test_stream = download_trace(client="IRIS",
                             starttime="2023-06-06T00:00:00",
                             timewindow="hour",
                             network="IU",
                             station="ANMO",
                             location="00",
                             channel="BHZ")

test_trace = test_stream[0]
test_trace.plot()

def divide_with_remainder(a, b):
    whole = round(a / b)
    remainder = a % b
    
    return whole, remainder

def cut_traces_into_windows(trace, windowlength, save=False):
    starttime = trace.stats['starttime']
    endtime = trace.stats['endtime']
    delta = trace.stats['delta']
    npts = trace.stats['npts']
    
    num_windows, window_remainder = divide_with_remainder(npts, (windowlength / delta))
    
    if window_remainder != 0:
        print('Warning: Amount of time downloaded not perfectly visible by the desired cut window length') 
        print('The final window will be shorter than the desired length')
        print(f'Desired window length: {windowlength} seconds')
        print(f'Length of final window: {window_remainder * delta}')
        
        endtime_int = endtime - (window_remainder * delta)
    else:
        endtime_int = endtime

    total_time = endtime_int - starttime + delta
    
    start_time_list, end_time_list = get_ambient_windows(starttime = starttime,
                                                         time_window = windowlength,
                                                         total_time = total_time,
                                                         delta = delta)
    
    if window_remainder != 0:
        start_time_list.append(end_time_list[-1])
        end_time_list.append(end_time_list[-1] + (window_remainder * delta))
    
    return start_time_list, end_time_list

start_time_list, end_time_list = cut_traces_into_windows(test_trace,600)
print(end_time_list)
    
    
    
    
    
    

