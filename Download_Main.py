# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.download_trace import download_trace
from ambient_download.cut_data import cut_traces_into_windows
from ambient_download.save_streamv2 import save_stream
from obspy import UTCDateTime
import obspy


def main():
    
    days = 15
    start_day = UTCDateTime("2023-06-06T00:00:00.000")
    
    stream = obspy.core.stream.Stream()
    
    for day in range(days):
        starttime = start_day + (15*86400)
        current_stream = download_trace(client="IRIS",
                                        network="IU",
                                        station="ANMO",
                                        location="00",
                                        channel="BHZ",
                                        starttime=starttime,
                                        timewindow = 86400)
        stream.append(current_stream)
    
    print('Successfully downloaded data')
    
    for trace in range(len(stream)):
        cut_stream = cut_traces_into_windows(trace, 3600)
        
        sort_method_list = ['station','year','julday']
        
        save_stream(stream=cut_stream,sort_method=sort_method_list,adding_data=True)
    
    print('Successfully saved traces')
    
if __name__ == '__main__':
    main()
    