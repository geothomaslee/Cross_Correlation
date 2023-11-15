#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Nov 14 22:55:03UTC 2023

@author: thomaslee
"""
import matplotlib.pyplot as plt
import numpy as np

def offset_view(a, b, offset):
    L = len(a)

    a_zeroes = np.concatenate(np.zeros(L), a)
    b_zeroes = np.concatenate(np.zeros(offset + L), b, np.zeroes(offset - L))

    lags = np.arange(-L, L, 1)
    fig, axs = plt.subplots(2, 1)

    axs[1].plot(x=lags,y=a_zeroes)
    axs[2].plot(x=lags,y=b_zeroes)
