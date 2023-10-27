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
    
    npts=trace1.stats['npts']
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
    print(type(meta))
    meta['network1'] = trace1.stats['network']
    meta['station1'] = trace1.stats['station']
    meta['network2'] = trace2.stats['network']
    meta['station2'] = trace2.stats['station']
    meta['year'] = trace1.stats['starttime'].year
    meta['julday'] = trace1.stats['starttime'].julday
    meta['hour'] = trace1.stats['starttime']
    
    return xcorr_times, xcorr, meta
   
def multi_correlate(pair_list,low,high=None,time_method='points'):
    xcorr_list = []
    
    for pair in pair_list:
        xcorr, xcorr_times, meta = cross_correlate_ambient_noise(pair,low,high,time_method)
        
    
    

        
    
    
    
    
    
""" 
def create_correlation_trace():
    # Creates a trace with the ambient times and the completed function
    pass
"""