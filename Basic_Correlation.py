#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:31:46 2023

@author: thomaslee
"""

import numpy as np
import matplotlib.pyplot as plt

# Generate three vectors of length 10 with values randomly between 1 and 10
a = np.random.uniform(low=-1,
                      high=1,
                      size=(10,))

b = np.random.uniform(low=-1,
                      high=1,
                      size=(10,))

c = np.random.uniform(low=-1,
                      high=1,
                      size=(10,))

x = [*range(0, len(a), 1)] # Time-step for made up time series 


# Plotting the correlation functions

fig, ax = plt.subplots(3, 1, figsize=(12, 6))

ax[0].plot(x, a,'--', label='a')
ax[0].set_title('Time-Series A')

ax[1].plot(x, b,'--', label='b')
ax[1].set_title('Time-Series B')

ax[2].plot(x, c,'--', label='c')
ax[2].set_title('Time-Series C')


def cross_correlation(a, b):
    """
    a: numpy vector of length n
    b: numpy vector of length n
    
    Returns: un-normalized cross-correlation values
    
    Cross-correlation is at its core, just multipyling corresponding values
    (meaning they have the same index) between two vectors of the same length,
    where the values within the vector are just the y-value of the time-series.
    
    The cross-correlation value is the SUM of the product of each corresponding
    values between the two time-series.
    
    Note - it is unitless! It's just a relative comparison of how similar two
    functions are. 
    
    Another note - it is also suspectible to outlier values! If a single value
    in one matrix is abnormally high or low, it will far outweigh the rest
    of the values contributing to the sum. This means that it will overpower
    what's happening on average between the two functions. In more technical
    terms, cross-correlation is highly suspectible to the power of the functions.
    
    This is why normalized cross-correlation is much better in practice.
    """
    cross_correlation = 0 # Begin with a value of 0
    
    for index in range(len(a)):
        add_cross_correlation = a[index] * b[index]
        cross_correlation += add_cross_correlation
        
    return cross_correlation

print(f'Cross Correlation between Vectors A and B: {cross_correlation(a, b)}')
print(f'Cross Correlation between Vectors A and C: {cross_correlation(a, c)}')
print(f'Cross Correlation between Vectors B and C: {cross_correlation(b, c)}')


# Cross correlation of trig functions to better visualize correlation

time_step = 0.1 # Play around with the time step!
phase_shift = 1 # Play around with the phase_shift of the second function!

time_series = np.arange(0, 10, 0.1)
                      
cos_func = np.cos(time_series - phase_shift)
sin_func = np.sin(time_series)

fig, ax = plt.subplots(2, 1, figsize=(12, 6))

ax[0].plot(time_series, cos_func)

ax[1].plot(time_series, sin_func)

fig.suptitle(f'Cross-Correlation: {cross_correlation(cos_func, sin_func)}')


           

        
        
    
    



