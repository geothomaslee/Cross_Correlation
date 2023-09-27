#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:52:22 2023

@author: thomaslee
"""

import matplotlib.pyplot as plt
import numpy as np


time_series = np.arange(0, 10, 0.1)

lag_index = np.arange(-len(time_series), len(time_series), 1)

func_1 = np.cos(time_series)
func_2 = np.sin(time_series)


