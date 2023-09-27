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



def cross_correlation(func_1, func_2, time):
    zeros_vector = np.zeros((len(time),))
    
    zeroed_func_1 = np.concatenate((zeros_vector, func_1, zeros_vector))
    
    return zeroed_func_1

test = cross_correlation(func_1, func_2, time_series)
print(test)
print(type(test))
print(test.shape)
    
    
        





