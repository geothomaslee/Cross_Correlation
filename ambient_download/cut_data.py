# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 12:47:52 2023

@author: tlee4
"""

from get_ambient_times import get_ambient_windows
from seis_download import download_seismic_data

test_stream = download_seismic_data(client="IRIS",
                                   starttime="2023-06-06T00:00:00",
                                   timewindow=86400,
                                   network="IU",
                                   station="ANMO",
                                   location="00",
                                   channel="BHZ")

test_trace = test_stream[0]

#def cut_traces_into_windows(trace):
    
    

