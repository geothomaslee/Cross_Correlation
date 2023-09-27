#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:52:22 2023

@author: thomaslee
"""

import matplotlib.pyplot as plt
import numpy as np

scaling_factor = 1

time_series = np.arange(0, 10, 0.1)

func_1 = np.cos(time_series)
func_2 = np.sin(time_series)

# Plotting the functions
fig, ax = plt.subplots(2, 1, figsize=(12, 6))

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

def cross_correlation(func_1, func_2, time):
    """
    a: numpy vector of length n
    b: numpy vector of length n
    
    Returns: un-normalized correlation values
    ---------
    See Basic_Correlation.py for notes on how this function works
    """
    zeros_vector = np.zeros((len(time),))
    
    # Centers the time_series in a new matrix with zeros on either end
    # to a distance equal to the length of func_2
    
    func_1_full = np.concatenate((zeros_vector, func_1, zeros_vector))
    
    lag_index = np.arange(0, len(func_1_full), 1)
    
    for lag in lag_index:
        # Figuring out how much empty space we have to the left and right
        # of func_2 as we sweep it from left to right
        lag_left = np.zeroes((lag,))
        lag_right = np.zeroes((len(func_1_full) - lag - len(func_1),))
        
        func_2_positioned = np.concatenate((lag_left, func_2, lag_right))
        
    
        
        
    
    


test = cross_correlation(func_1, func_2, time_series)

    
    
        





