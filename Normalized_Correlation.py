# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:59:05 2023

@author: tlee4
"""

import numpy as np
import matplotlib.pyplot as plt

scaling_factor = 15 # Play around with this!!

# Creating two time-series data with identical shape but different powers

time_series = np.arange(0, 10, 0.1)

func_1 = np.cos(time_series)
func_2 = np.cos(time_series) * scaling_factor

# Plotting our two cosine functions with different amplitudes
fig, ax = plt.subplots(2, 1, figsize=(12, 6))

margin = scaling_factor * 1.1 # Margin is 10% larger than max amplitude

ax[0].plot(time_series, func_1)
ax[0].set_ylim((-1 * margin), margin)

ax[1].plot(time_series, func_2)
ax[1].set_ylim((-1 * margin), margin)

def normalized_correlation(a, b):
    """
    Parameters
    ----------
    a : np.array
        Y-values of the first time-series stored in a numpy vector.
    b : np.array
        Y-values of the secod time-series stored in a numpy vector.

    Returns normalized correlation value as an integer or float.
    
    Returns un-normalized correlation value.
    -------
    Normalized correlation does conceptually the same thing as the
    regular correlation (see basic correlation for explanation) but
    divides the correlation by a normalizing factor. The normalizing
    factor is calculated based on the power of the function so that two functions
    with the same shape but different powers give back a correlation that compares
    the shapes of the function, but doesn't care about the amplitude. The
    normalized correlation will always be between -1 and 1.

    """
    correlation = 0
    norm_sum_a = 0
    norm_sum_b = 0
    for index in range(len(time_series)):
        add_correlation = a[index] * b[index]
        add_norm_sum_a = a[index] ** 2
        add_norm_sum_b = b[index] ** 2
        
        correlation += add_correlation
        norm_sum_a += add_norm_sum_a
        norm_sum_b += add_norm_sum_b
    
    normalizing_factor = np.sqrt(norm_sum_a * norm_sum_b)
    normalized_correlation = correlation / normalizing_factor
    
    return normalized_correlation, correlation

ex_norm_cc, ex_cc= normalized_correlation(func_1, func_2)

fig.suptitle(f'Normalized Correlation: {ex_norm_cc}, Unnormalized: {ex_cc}')

