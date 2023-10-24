# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:52 2023

@author: tlee4
"""

import obspy
from obspy import UTCDateTime
import math

def divide_with_remainder(a, b):
    whole = math.floor(a / b)
    remainder = a % b
    
    return whole, remainder

def get_ambient_windows(starttime, time_window, total_time, delta, cut_endpoint = False):
    """
    Parameters
    ----------
    starttime : string
        Start time as a string in the format year-mm-ddThr-mn-sc.000
    time_window : integer
        Desired window length as in integer in seconds.
    total_time : integer
        Overall time length as in integer in seconds.
    delta : float or integer
        The sampling rate of the instrument.
    cut_endpoint : bool
        If enabled, will remove the last endpoint to avoid traces overlapping.

    Returns
    -------
    start_time_list : list
        List of start times for the ambient windows
    end_time_list : list
        List of end times for the ambient windows
    """
    starttime_int = UTCDateTime(starttime) # UTCDateTime object of the starttime
    start_time_list = [starttime_int] # Begins the start_time_list
    
    # Creates the first end_time, because this script works by just adding
    # the time_window to the previous time given in the start and end lists
    
    # Also cuts endpoint off if specified by cut_endpoint
    if cut_endpoint == True:
        end_time_list = [(starttime_int + time_window - delta)]
    elif cut_endpoint == False:
        end_time_list = [(starttime_int + time_window)]
    elif type(cut_endpoint) != bool:
        raise TypeError('Cut_endpoint must be either True or False')
        
    # Checks to see if the time length can be divided by the time windows 
    if (total_time % time_window) == 0:
        num_windows = int(total_time / time_window)
    else:
        raise ValueError('Time length must be evenly divisible by time window')
    
    for i in range(num_windows - 1):
        new_start_time = start_time_list[-1] + time_window
        start_time_list.append(new_start_time)
        
        new_end_time = end_time_list[-1] + time_window
        end_time_list.append(new_end_time)
    
    return start_time_list, end_time_list

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
    