# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.download_trace import download_trace
from ambient_download.cut_data import cut_traces_into_windows
from ambient_download.save_streamv2 import save_stream


def main():
    stream = download_trace(client="IRIS",
                            network="IU",
                            station="ANMO",
                            location="00",
                            channel="BHZ",
                            starttime="2023-06-06T00:00:00.000",
                            timewindow = 86400)
    
    cut_stream = cut_traces_into_windows(stream[0],3600)
    
    
    sort_method_list = ['station','year','julday']
    
    save_stream(stream=cut_stream,sort_method=sort_method_list)
    
if __name__ == '__main__':
    main()
    