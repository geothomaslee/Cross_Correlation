# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:27:43 2023

@author: tlee4
"""

def get_ambient_windows(starttime, time_window, time_length):
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
    
    time_list = [starttime_int]
    num_windows = time_length / time_window
    print(num_windows)
    
    for i in range(num_windows - 1):
        new_time = time_list[-1] + time_window
        time_list.append(new_time)
    
    return time_list
    
test_ambient_windows = get_ambient_windows("2020-09-15T05:00:00.000", 60, 360)
print(test_ambient_windows)