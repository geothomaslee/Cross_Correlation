# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.download_trace import download_trace
from ambient_download.cut_data import cut_traces_into_windows
from ambient_download.save_stream import save_stream
import obspy
import time
import numpy as np
from tqdm import tqdm
from obspy import UTCDateTime


"""
starttime = "2022-01-01T00:00:00.000"
endtime = "2022-02-01T00:00:00.000"
stream = download_trace(client="IRIS",
                              network="IU",
                              station="ANMO",
                              location="00",
                              channel="BHZ",
                              starttime=starttime,
                              timewindow=endtime)

stream.write('./test_data_2','MSEED')
"""


def main():
    starttime = "2022-01-01T00:00:00.000"
    endtime = "2022-02-01T00:00:00.000"
    
    stream = obspy.read('./test_data_2.mseed')

    """
    stream = download_trace(client="IRIS",
                                  network="IU",
                                  station="ANMO",
                                  location="00",
                                  channel="BHZ",
                                  starttime=starttime,
                                  timewindow=endtime)
    """
                         
    cut_stream = cut_traces_into_windows(stream,windowlength=3600)
    
    sort_method_list = ['station','year','julday']
    
    save_stream(stream=cut_stream,main_folder='./Downloaded_Traces',
                sort_method=sort_method_list, adding_data=True)
    
    print('Successfully saved traces')
    cut_stream.clear()
    
if __name__ == '__main__':
    main()
