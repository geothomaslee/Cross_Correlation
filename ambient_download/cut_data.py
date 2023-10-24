# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:52 2023

@author: tlee4
"""

from get_ambient_times import get_ambient_windows
from download_trace import download_trace
import obspy
import math
import time

test_stream = download_trace(client="IRIS",
                             starttime="2023-06-06T00:00:00",
                             timewindow=86400,
                             network="IU",
                             station="ANMO",
                             location="00",
                             channel="BHZ")

test_trace = test_stream[0]
test_trace.plot()

def divide_with_remainder(a, b):
    whole = math.floor(a / b)
    remainder = a % b
    
    return whole, remainder

def cut_traces_into_windows(trace, windowlength, save=False):
    
    window_calc_time = time.perf_counter()
    
    starttime = trace.stats['starttime']
    endtime = trace.stats['endtime']
    delta = trace.stats['delta']
    npts = trace.stats['npts']
    
    # Checks to see if total time in trace is divisible by desired window length
    num_whole_windows, window_remainder = divide_with_remainder(npts, (windowlength / delta))
    
    if window_remainder != 0:
        print('Warning: Amount of time downloaded not perfectly visible by the desired cut window length') 
        print('The final window will be shorter than the desired length')
        print(f'Desired window length: {windowlength} seconds')
        print(f'Length of final window: {window_remainder * delta}')
        
        # Correction to remove the remainder because get_ambient_windwos can't handle it
        endtime_int = endtime - (window_remainder * delta)
        num_windows = num_whole_windows + 1 # Total windows includes one partial window
    else:
        endtime_int = endtime
        num_windows = num_whole_windows

    # Total time to be fed to get_ambient_windows which can't deal with remainders
    total_time = endtime - starttime + delta
    total_time_whole = endtime_int - starttime + delta
        
    print(f'Cutting {total_time} seconds of data into {num_windows} windows')
    
    start_time_list, end_time_list = get_ambient_windows(starttime = starttime,
                                                         time_window = windowlength,
                                                         total_time = total_time_whole,
                                                         delta = delta)
    
    # This adds back in the remainder time length
    if window_remainder != 0:
        start_time_list.append(end_time_list[-1])
        end_time_list.append(end_time_list[-1] + (window_remainder * delta))
       
    print(f'Window calculation time: {time.perf_counter() - window_calc_time}')
    
    cut_time = time.perf_counter()
    
    int_func_stream = obspy.core.stream.Stream()
    
    for i in range(num_windows):
        cut_start = start_time_list[i]
        cut_end = end_time_list[i]
        cut_trace = trace.copy()
        
        cut_trace.trim(cut_start,cut_end)
        
        int_func_stream.append(cut_trace)
        
    print(f'Cut time: {time.perf_counter() - cut_time}')
        
    return int_func_stream
        
cut_stream = cut_traces_into_windows(test_trace,3600)
    
    
    
    
    

