# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 14:40:59 2023

@author: tlee4
"""

#import glob as glob
import shutil
import os

from download_trace import download_trace

def save_stream_traces(stream,main_folder="./Downloaded_Traces",format="mseed",
                       sort_method=None, force_overwrite=False):
    
    if sort_method == None:
        raise ValueError('A list of sorting methods must be given')
    
    num_traces = len(stream)
    
    # Checks if input is a stream
    if type(stream.count()) != int:
        raise TypeError('Input stream is almost certainly not an Obspy stream')
        
    if type(sort_method) == list:
        sort_method_list = sort_method
    elif type(sort_method) == str:
        sort_method_list = [sort_method]
    else:
        raise TypeError('Expected list of strings, or single string')
    
    # Checks if data directory is empty, and raises an error if it isn't. If 
    # force_overwrite is True, then will delete the data directory
    if os.path.isdir(main_folder):
        if len(os.listdir(main_folder)) != 0:
            if force_overwrite:
                shutil.rmtree(main_folder)
            else:
                raise RuntimeError('Data directory is not empty and may contain other data')
    else: # Creates the directory folder if
        os.makedirs(main_folder)
        
    acceptable_sort_method_list = ["starttime", "endtime", 
                                   "network", "station",
                                   "location", "channel"]
    
    
    if all(method in acceptable_sort_method_list for method in sort_method_list):
        pass
    else:
        raise ValueError('Invalid sort method included in sort_method. See help for acceptable methods')
     
    for trace_index in range(num_traces):
        trace = stream[trace_index]
        
        # Pulls some basic metadata from the trace
        station = trace.meta['station']
        network = trace.meta['network']
        location = trace.meta['location']
        channel = trace.meta['channel']
        starttime = trace.meta['starttime']
        endtime = trace.meta['endtime']
        
        """
        start_datetime = starttime.datetime
        
        year = start_datetime.year
        month = start_datetime.month
        day = start_datetime.day
        hour = start_datetime.hour
        minute = start_datetime.minute
        """
        
        trace_directory = f'{main_folder}./'
        for sub_dir in sort_method_list:
            trace_directory.append(sub_dir)
                
        print(trace_directory)
        

test_stream = download_trace(client="IRIS",
                             starttime="2023-06-06T00:00:00.000",
                             timewindow=3600,
                             network="IU",
                             station="ANMO",
                             location="00",
                             channel="BHZ")
    
    
test_sort_list = ['station','network']
save_stream_traces(stream=test_stream,
                   sort_method = test_sort_list)
        
        
"""
        if sort_method == "starttime":
            sort_folder = start_time_formatted
        else:
            sort_folder = trace.meta[sort_method]
            
        sort_folder_path = f'{main_folder}/{sort_folder}'
        
        if not os.path.isdir(sort_folder_path):
            os.makedirs(sort_folder_path)
        
        filename = f'{station}.{channel}.{start_time_formatted}.{format}'
        
        trace.write(f'./{sort_folder_path}/{filename}')
"""
        
       
        
        
        
        
        
        