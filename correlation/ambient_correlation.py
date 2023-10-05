# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 08:48:56 2023

@author: tlee4
"""
import os

def find_stations(stationfolder):
    """
    Parameters
    ----------
    stationfolder : string
        Path to the folder containing station data.

    Returns
    -------
    None.

    """
    station_list = os.listdir(stationfolder)
    