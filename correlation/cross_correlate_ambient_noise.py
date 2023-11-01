# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 22:34:22 2023

@author: tlee4
"""

import obspy
import numpy as np
from obspy.signal.cross_correlation import correlate
from obspy.signal.filter import bandpass
import matplotlib.pyplot as plt
from statistics import mode

def create_ambient_times(npts,delta,method='points'):
    if method == 'points':
        times = np.arange((0-npts),npts+1,1)
    elif method == 'seconds':
        seconds = npts * delta
        times = np.arange((0 - seconds), seconds+delta, delta)
        
    return times

def cross_correlate_ambient_noise(pair,low,high=None,time_method='points'):
    trace1 = obspy.read(pair[0])[0]
    trace2 = obspy.read(pair[1])[0]
    
    npts1=trace1.stats['npts']
    npts2=trace2.stats['npts']
    
    if npts1 == npts2:
        npts = npts1
    else:
        print(f'Files have different number of points. Using npts1 {npts1}')
        npts = npts1
    
    delta=trace1.stats['delta']
    sampling_rate = 1/delta
    
    if high == None:
        high_freq = (sampling_rate / 2) - delta
    elif type(high) == int or type(high) == float:
        high_freq = high
    else:
        raise TypeError('High must be int or float')
    
    trace1_filtered = trace1.detrend()
    trace1_filtered = bandpass(trace1,freqmin=low,freqmax=high_freq,
                               df=sampling_rate,corners=4)
    
    trace2_filtered = trace2.detrend()
    trace2_filtered = bandpass(trace2,freqmin=low,freqmax=high_freq,
                               df=sampling_rate,corners=4)
    
    xcorr = correlate(trace1_filtered, trace2_filtered,normalize=None,shift=npts)
    
    xcorr_times = create_ambient_times(npts,delta,time_method)
    
    meta = {}
    meta['network1'] = trace1.stats['network']
    meta['station1'] = trace1.stats['station']
    meta['network2'] = trace2.stats['network']
    meta['station2'] = trace2.stats['station']
    meta['year'] = trace1.stats['starttime'].year
    meta['julday'] = trace1.stats['starttime'].julday
    meta['hour'] = trace1.stats['starttime']

    return xcorr, xcorr_times, meta

def check_correlation_length(xcorr_list):
    """
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
   
def multi_correlate(pair_list,low,high=None,time_method='points'):
    """
    Parameters
    ----------
    pair_list : list of length-2 lists of strings
        List of lists, each sub-list being a pair of strings giving the file path
        to the files to be cross-correlation
    low : int or float
        Low end of bandpass filter. Suggested 0.05Hz = 20 second period.
    high : int or float, optional
        High end of bandpass filter. Defaults to Nyquist frequency of the files.
    time_method : string, optional
        'points' or 'seconds': Gives the list of times as points or seconds.

    Returns
    -------
    xcorr_list_fixed : list of numpy.ndarray
        List containing the cross-correlation functions for each window given
        as a numpy array.
    xcorr_times : numpy.ndarray
        Times for the cross-correlation function, given as a numpy array.
    """
    xcorr_list = []
    
    for pair in pair_list:
        xcorr, xcorr_times, meta = cross_correlate_ambient_noise(pair,low,high,time_method)
        xcorr_list.append(xcorr)
        
    xcorr_list_fixed = check_correlation_length(xcorr_list)
    
    return xcorr_list_fixed, xcorr_times

def xcorr_stack(xcorr_list):
    xcorr_stack = sum(xcorr_list) / len(xcorr_list)
    return xcorr_stack

