# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:59:05 2023

@author: tlee4
"""

import numpy as np
import matplotlib.pyplot as plt

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
    for index in range(len(a)):
        add_correlation = a[index] * b[index]
        add_norm_sum_a = a[index] ** 2
        add_norm_sum_b = b[index] ** 2
        
        correlation += add_correlation
        norm_sum_a += add_norm_sum_a
        norm_sum_b += add_norm_sum_b
    
    normalizing_factor = np.sqrt(norm_sum_a * norm_sum_b)
    normalized_correlation = correlation / normalizing_factor
    
    return normalized_correlation

