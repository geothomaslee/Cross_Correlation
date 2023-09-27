#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:52:22 2023

@author: thomaslee
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy

scaling_factor = 5
# Scaling factor to change amplitude of the first function
# Set to 1 by default, but play around with this to see how the power of the
# functions affects the correlation

delta = 0.01 # Time-step of time-series, AKA instrument sampling rate
window_length = 60 # Correlation length of the window in seconds

# A good example of what real data may look like is a 3600 second window
# with a delta of 0.01, representing an hour of data sampling at 100Hz

time_series = np.arange(0, window_length, delta)

func_1 = np.cos(time_series) * scaling_factor
func_2 = np.sin(time_series)

# Plotting the functions
fig, ax = plt.subplots(3, 1, figsize=(12, 6))

margin = scaling_factor * 1.1 # Margin is 10% larger than max amplitude

ax[0].plot(time_series, func_1)
ax[0].set_ylim((-1 * margin), margin)

ax[1].plot(time_series, func_2)
ax[1].set_ylim((-1 * margin), margin)

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



# Calculating the cross-correlation function for the two example functions
cross_correlation, correlation_time_series = cross_correlation(func_1, func_2, time_series, delta)

# Plotting the correlation next to the original functions
ax[2].plot(correlation_time_series, cross_correlation)

# Calculating the correlation function via Scipy to verify
scipy_correlation = scipy.signal.correlate(func_1, func_2)

# Has 199 values but should have 200, where 200th value is 0
scipy_correlation_len_fix = np.concatenate((scipy_correlation, np.zeros(1,)))

# Plotting our correlation vs. Scipy correlation
comp_fig, comp_ax = plt.subplots(2, 1, figsize=(12,6))

comp_ax[0].plot(correlation_time_series, cross_correlation)
comp_ax[0].set_title('Correlation From This Script')

comp_ax[1].plot(correlation_time_series, scipy_correlation_len_fix)
comp_ax[1].set_title('Correlation From Scipy')

comp_fig.suptitle('Verification of Correct Correlation')



    



    
    
        





