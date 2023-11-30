# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 22:34:22 2023

@author: tlee4
"""

import obspy
import numpy as np
from obspy.signal.cross_correlation import correlate
from statistics import mode

def create_ambient_times(npts,delta,method='points'):
    """
    Parameters
    ----------
    npts : int
        Number of points in the file.
    delta : int or float
        Time-step between points (40 samples per second = delta of 0.0125).
    method : string, optional
        'points' or 'seconds': Gives the time values as points or seconds

    Returns
    -------
    times : np.ndarray
        NumPy array containing the times for the cross-correlation function.

    """
    if method == 'points':
        times = np.arange((0-npts),npts+1,1)
    elif method == 'seconds':
        seconds = npts * delta
        times = np.arange((0 - seconds), seconds+delta, delta)
        
    return times

def one_bit_normalization(array):
    normalized_list = []
    for value in enumerate(array):
        if value > 0:
            new_val = 1
        elif value < 0:
            new_val = -1
        elif value == 0:
            new_val = 0
        normalized_list.append(new_val)
        
    normalized_array = np.asarray(normalized_list)
    
    return normalized_array
        

def filter_stream(stream,normalize=True):
    """
    Cross-correlation pre-processing method after Jiang et. al., 2023
    
    Detrend, max 0.1% taper, 4-pole 2-pass Butterworth bandpass from 0.02 to 
    0.5 Hz, downsample to 1 Hz

    Parameters
    ----------
    stream : obspy.core.stream.Stream
        ObsPy stream containing trace(s) to be filtered.
    normalize : bool, optional
        If set true, will normalize each trace by its maximum. Default is true.

    Returns
    -------
    stream : obspy.core.stream.Stream
        ObsPy stream containing the filtered trace(s).
    """
    stream.detrend()
    stream.taper(0.1)
    stream.filter('bandpass',freqmin=0.02,freqmax=0.5,corners=4)
    stream.resample(1)
    
    if normalize == True:
        stream.normalize()
    
    return stream

def cross_correlate_ambient_noise(pair,time_method='points',normalize=True):
    """
    Parameters
    ----------
    pair : list, length 2, of strings
        List containung the path to the two files to be cross-correlated.
    time_method : string, optional
        'points' or 'seconds': Gives the time values as points or seconds.

    Returns
    -------
    xcorr : numpy.ndarray
        Cross-correlation function given as a numpy array.
    xcorr_times : numpy.ndarray
        Times for the cross-correlation function.
    meta : dict
        Dictionary containing meta-data for the correlation.
    """
    stream = obspy.read(pair[0])
    stream.append(obspy.read(pair[1])[0])
    
    stream_filtered = filter_stream(stream,normalize=normalize)
    
    npts = stream_filtered[0].stats['npts']
    delta_new = stream_filtered[0].stats['delta']
    
    stream.detrend() # Remove trend again, after Jiang et. al., 2023
    
    xcorr = correlate(stream_filtered[0], stream_filtered[1],shift=npts,normalize=None)
    
    xcorr_times = create_ambient_times(npts,delta_new,time_method)
    
    meta = {}
    meta['network1'] = stream_filtered[0].stats['network']
    meta['station1'] = stream_filtered[0].stats['station']
    meta['network1'] = stream_filtered[1].stats['network']
    meta['station1'] = stream_filtered[1].stats['station']
    meta['year'] = stream_filtered[0].stats['starttime'].year
    meta['julday'] = stream_filtered[0].stats['starttime'].julday
    meta['hour'] = stream_filtered[0].stats['starttime']

    return xcorr, xcorr_times, meta


def check_correlation_length(xcorr_list):
    """
    Makes sure that all traces have the same length because occasionally they
    come out a point or two less than they should be. If this is the case, just
    adds zeros to bring it up to the proper length because data at these 
    extremes has mostly been tapered out anyway.
    
    Parameters
    ----------
    xcorr_list : list of numpy.ndarray
        List of cross-correlation functions given as numpy arrays
        
    Returns
    -------
    xcorr_list : numpy.ndarray
        Numpy array containing a single stacked correlation function.
    """
    len_list = []
    for i, xcorr in enumerate(xcorr_list):
        len_list.append(len(xcorr))
        
    npts_expected = mode(len_list)

    for i, xcorr in enumerate(xcorr_list):
        if len(xcorr) == npts_expected:
            pass
        else:
            xcorr_new = xcorr.copy()
            add_pts = npts_expected - len(xcorr)
            for add in range(add_pts):
                xcorr_new = np.append(xcorr_new, 0)
                
            xcorr_list[i] = xcorr_new
            
    return xcorr_list
   
def multi_correlate(pair_list,time_method='points',normalize=True):
    """
    Parameters
    ----------
    pair_list : list of length-2 lists of strings
        List of lists, each sub-list being a pair of strings giving the file path
        to the files to be cross-correlation.
    time_method : string, optional
        'points' or 'seconds': Gives the list of times as points or seconds.

    Returns
    -------
    xcorr_list_fixed : list of numpy.ndarray
        List containing the cross-correlation functions for each window given
        as a numpy array. _fixed refers to it having been run through
        check_correlation_length, see check_correlation_length for details.
    xcorr_times : numpy.ndarray
        Times for the cross-correlation function, given as a numpy array.
    """
    xcorr_list = []
    
    for pair in pair_list:
        xcorr, xcorr_times, meta = cross_correlate_ambient_noise(pair,time_method,normalize=normalize)
        xcorr_list.append(xcorr)
        
    xcorr_list_fixed = check_correlation_length(xcorr_list)
    
    return xcorr_list_fixed, xcorr_times

def running_average_filter(xcorr, xcorr_times, avg_window=20):
    """
    Parameters
    ----------
    xcorr : numpy.ndarray
        Cross-correlation function in a NumPy array.
    xcorr_times : numpy.ndarray
        Times for the cross-correlation function.
    avg_window : int, optional
        Number of points to include in the moving average filter. 
        The default is 20.

    Returns
    -------
    xcorr_averaged : numpy.ndarray
        Cross-correlation smoothed using a moving average.
    xcorr_averaged_times : numpy.ndarray
        Times, but with the first and last avg_window/2 points removed because
        this moving average filter just starts at the first point with sufficient
        number of points on either side of the current point to calculate the
        moving average.
    """
    xcorr_averaged = []
    
    npts = len(xcorr)
    
    lower_bound_all = int(avg_window / 2)
    upper_bound_all =  int(npts - (avg_window / 2))
    
    for i in np.arange(lower_bound_all, upper_bound_all, 1):
        
        int_i = int(i)
        upper_bound = int_i + avg_window
        avg_window_values = xcorr[int_i:upper_bound]
        avg = np.mean(avg_window_values)
        
        xcorr_averaged.append(avg)
        
        
    xcorr_averaged_times=xcorr_times[lower_bound_all:upper_bound_all]
        
    return xcorr_averaged, xcorr_averaged_times
        
def xcorr_stack(xcorr_list):
    """
    Parameters
    ----------
    xcorr_list : list of numpy.ndarray
        List of cross-correlation functions for each time window given as 
        numpy arrays.

    Returns
    -------
    xcorr_stack : numpy.ndarray
        Numpy array containing the stacked cross-correlation function.
    """
    xcorr_stack = sum(xcorr_list) / len(xcorr_list)
    return xcorr_stack

