# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:27:43 2023

@author: tlee4
"""

from obspy import UTCDateTime

def get_ambient_windows(starttime, time_window, time_length, delta):
    """
    Parameters
    ----------
    starttime : string
        Start time as a string in the format year-mm-ddThr-mn-sc.000
    time_window : integer
        Desired window length as in integer in seconds.
    time_length : integer
        Overall time length as in integer in seconds.

    Returns
    -------
    ambient_time_windows : list
        List of starttimes for the ambient time windows
    """
    starttime_int = UTCDateTime(starttime)
    
    start_time_list = [starttime_int]
    end_time_list = [(starttime_int + time_window - delta)]
    
    num_windows = int(time_length / time_window)
    
    for i in range(num_windows - 1):
        new_start_time = start_time_list[-1] + time_window
        start_time_list.append(new_start_time)
        
        new_end_time = end_time_list[-1] + time_window
        end_time_list.append(new_end_time)
    
    return start_time_list, end_time_list