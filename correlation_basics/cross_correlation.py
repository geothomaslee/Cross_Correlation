#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:52:22 2023

@author: thomaslee
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy

def correlation(a, b):
    """
    a: numpy vector of length n
    b: numpy vector of length n
    
    Returns: un-normalized correlation values
    ---------
    See Basic_Correlation.py for notes on how this function works
    """
    correlation = 0 # Begin with a value of 0
    
    for index in range(len(a)):
        add_correlation = a[index] * b[index]
        correlation += add_correlation
        
    return correlation

def cross_correlation(func_1, func_2, time, delta):
    """
    func_1: numpy array of length n
    func_1: numpy array of length n
    time: numpy array of length n containing the times for the two functions,
    which should be the same for both
    delta: the time-step of the two functions, which when working with real
    data should be the sampling rate of the isntrument
    
    Returns: cross_correlation, numpy array containing the time-series of the 
    cross-correlation function
    
    Returns: correlation_time_series, a numpy array containing the correct 
    times for the cross-correlation function
    ---------
    """
    zeros_vector = np.zeros((len(func_1)))
    
    # Centers the time_series in a new matrix with zeros on either end
    # to a distance equal to the length of func_2
    
    func_1_full = np.concatenate((zeros_vector, func_1, zeros_vector))
    
    lag_index = np.arange(0, len(func_1) * 2, 1)
    
    cross_correlation = []
    
    for lag in lag_index:
        # Figuring out how much empty space we have to the left and right
        # of func_2 as we sweep it from left to right
        lag_left = np.zeros((lag,))
        
        ## Check when the right lag ends
        
        if (len(func_1_full) - lag - len(func_1)) >= 0:
            lag_right = np.zeros((len(func_1_full) - lag - len(func_1),))
            func_2_positioned = np.concatenate((lag_left, func_2, lag_right))
        else:
            func_2_positioned = np.concatenate((lag_left, func_2))
            
        correlation_val = correlation(func_1_full, func_2_positioned)
        
        cross_correlation.append(correlation_val)

    # Creating the times for the correlation value, which includes the original
    # times but also the same length of time before and after added to the
    # overall time window
    
    time_span = time[-1] - time[0] + delta

    time_left = time[0] - time_span
    #time_right = time[-1] + time_span + delta

    times_left = np.arange(time_left, time[0], delta)
    #times_right = np.arange((time[-1] + delta), time_right, delta)

    correlation_time_series = np.concatenate((times_left, time))

    return cross_correlation, correlation_time_series



    



    
    
        





