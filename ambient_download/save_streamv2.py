# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 14:40:59 2023

@author: tlee4
"""

#import glob as glob
import shutil
import os

def save_stream(stream,main_folder="./Downloaded_Traces",format="MSEED",
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
                                   "location", "channel",
                                   "julday","year"]
    
    
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
        
        julday = str(starttime.julday)
        year = str(starttime.year)
        hour = str(starttime.hour)
        
        trace_directory = f'{main_folder}./'
        
        # Creating the name of the sorting folder
        for i, sub_dir in enumerate(sort_method_list):
            sub_dir_val = locals()[sub_dir]
            # Pulls the value of the variable because name is given as string
            if i == (len(sort_method_list) -1): # Checks to not add ./ to last folder
                trace_directory = trace_directory + sub_dir_val
            else:
                trace_directory = trace_directory + sub_dir_val + '/'
                
        if os.path.isdir(trace_directory):
            pass
        else:
            os.makedirs(trace_directory)
                
        file_name = f'{network}.{station}.{year}.{julday}.{hour}.{format}'
        file_path_name = trace_directory + '/' + file_name
            
        trace.write(file_path_name,format=format)

