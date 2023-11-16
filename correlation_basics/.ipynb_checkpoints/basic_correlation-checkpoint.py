#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:31:46 2023

@author: thomaslee
"""

import numpy as np

def correlation(a, b):
    """
    a: numpy vector of length n
    b: numpy vector of length n
    
    Returns: un-normalized correlation values
    
    Correlation is at its core, just multipyling corresponding values
    (meaning they have the same index) between two vectors of the same length,
    where the values within the vector are just the y-value of the time-series.
    
    The correlation value is the SUM of the product of each corresponding
    values between the two time-series.
    
    Note - it is unitless! It's just a relative comparison of how similar two
    functions are. 
    
    Another note - it is also suspectible to outlier values! If a single value
    in one matrix is abnormally high or low, it will far outweigh the rest
    of the values contributing to the sum. This means that it will overpower
    what's happening on average between the two functions. In more technical
    terms, correlation is highly suspectible to the power of the functions.
    
    This is why normalized correlation is much better in practice.
    """
    correlation = 0 # Begin with a value of 0
    
    for index in range(len(a)):
        add_correlation = a[index] * b[index]
        correlation += add_correlation
        
    return correlation


           

        
        
    
    



