# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:27:43 2023

@author: tlee4
"""

from obspy import UTCDateTime

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