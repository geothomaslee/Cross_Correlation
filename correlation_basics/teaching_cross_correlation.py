#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Nov 14 22:55:03UTC 2023

@author: thomaslee
"""
import matplotlib.pyplot as plt
import numpy as np
from correlation_basics.basic_correlation import correlation

def full_correlation_function(a, b):
    L=len(a)
    lags = np.arange(-L, L, 1)
    
    correlation_list = []
    for offset in lags:
        a_zeros = np.zeros(L)
        a_full = np.concatenate((a_zeros, a, a_zeros))

        b_left_zeros = np.zeros(offset+L) # =0 when offset = -L, = 2L when offset is L
        b_right_zeros = np.zeros(L-offset)
        b_full = np.concatenate((b_left_zeros, b, b_right_zeros))
        
        current_correlation = correlation(a_full, b_full)
        correlation_list.append(current_correlation)
        
    return correlation_list
        

def correlate_interactive(a, b, offset):
    L=len(a)
    
    max = a.max
    min = a.min
    
    a_zeros = np.zeros(L)
    a_full = np.concatenate((a_zeros, a, a_zeros)) # np.concatenate requires inputs to be in a tuple or it returns a completely useless error message
    
    b_left_zeros = np.zeros(offset+L) # =0 when offset = -L, = 2L when offset is L
    b_right_zeros = np.zeros(L-offset)
    b_full = np.concatenate((b_left_zeros, b, b_right_zeros))
    
    current_correlation = correlation(a_full, b_full)
    
    full_correlation = full_correlation_function(a, b)
    
    lags = np.arange(-L, 2*L, 1)
    fig, axs = plt.subplots(3, 1)
    
    short_lags = np.arange(-L, L, 1)
    
    fig.tight_layout(pad=2)

    axs[0].plot(lags,a_full)
    axs[0].set_title('Function 1')
    
    axs[1].plot(lags,b_full)
    axs[1].set_title('Function 2')
    
    axs[2].plot(short_lags,full_correlation)
    axs[2].plot(offset,current_correlation,'ro')
    axs[2].set_title(f'Correlation Function, current value: {current_correlation}')
    
