# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:52 2023

@author: tlee4
"""

from get_ambient_times import get_ambient_windows
import obspy
import math

def divide_with_remainder(a, b):
    whole = math.floor(a / b)
    remainder = a % b
    
    return whole, remainder

def cut_traces_into_windows(trace, windowlength):
    """
    Parameters
    ----------
    trace : obspy.core.trace.Trace
        The ObsPy trace that you want to cut.
    windowlength : int
        length, in seconds, of the desired cut window.

    Returns
    -------
    int_func_stream : obspy.core.stream.Stream
        An ObsPy stream containing all of the cut traces
    """
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
       
    int_func_stream = obspy.core.stream.Stream()
    
    for i in range(num_windows):
        cut_start = start_time_list[i]
        cut_end = end_time_list[i]
        cut_trace = trace.copy()
        
        cut_trace.trim(cut_start,cut_end)
        
        int_func_stream.append(cut_trace)
        
    return int_func_stream
    