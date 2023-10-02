# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 14:40:59 2023

@author: tlee4
"""

#import glob as glob
import shutil
import os

def save_stream_traces(stream,main_folder="./Downloaded_Traces",format="mseed",
                       sort_method="station",
                       use_network=True,use_station=True,
                       use_location=False,use_channel=True,
                       use_starttime=True,use_endtime=False,
                       force_overwrite=False):

    """
    Parameters
    ----------
    stream : obspy.core.stream.Stream
        Obspy Stream containing the traces you wish to download.
        
    folder : string, optional
        The path of the main data folder that will contain your data.
        
        The default is "./Downloaded_Traces".
        
    format : string, optional
        File type for saved data. The default is MSEED.
        
    sort_method : string, optional
        Method for sorting the files into subdirectories within the main data
        folder. Method must be either starttime, endtime, network, station,
        location, or channel.
        
    force_overwrite : bool, optional
        If set to True, will forcibly delete any data that exists in the main
        folder before saving new data.
        
    use_starttime : bool, optional
        Include start time of the trace in the file name? The default is True.
    use_endtime : bool, optional
        Include the end time in the file name?. The default is False.
    use_network : bool, optional
        Include the network in the file name? The default is True.
    use_station : bool, optional
        Include the station in the file name? The default is True.
    use_location: bool, optional
        Include the channel location in the file name? The default is False.
    use_channel: bool, optional
        Include the channel in the file name> The default is True.

    Returns
    -------
    """
    
    num_traces = len(stream)
    
    if type(stream.count()) != int:
        raise TypeError('Input stream is almost certainly not an Obspy stream')
    
    if os.path.isdir(main_folder):
        if len(os.listdir(main_folder)) != 0:
            if force_overwrite:
                shutil.rmtree(main_folder)
            else:
                raise RuntimeError('Data directory is not empty and may contain other data')
    else:
        os.makedirs(main_folder)
        
    acceptable_sort_method_list = ["starttime", "endtime", 
                                   "network", "station",
                                   "location", "channel"]
    if sort_method not in acceptable_sort_method_list:
        raise ValueError('Invalid sort method. Use help to see valid sort methods')
    
    arguments = locals()
    name_use = {}
    
    for key in arguments:
        value = arguments[key]
        if type(value) == bool:
            if "use" in key:
                if value:
                    name_use[key] = ""
    
    for trace_index in range(num_traces):
        trace = stream[trace_index]
        
        station = trace.meta['station']
        network = trace.meta['network']
        location = trace.meta['location']
        channel = trace.meta['channel']
        starttime = trace.meta['starttime']
        endtime = trace.meta['endtime']
        
        start_datetime = starttime.datetime
        
        year = start_datetime.year
        month = start_datetime.month
        day = start_datetime.day
        hour = start_datetime.hour
        minute = start_datetime.minute
        
        if "use_endtime" in name_use:
            end_datetime = endtime.datetime
            year = end_datetime.year
            month = end_datetime.month
            day = end_datetime.day
            hour = end_datetime.hour
            minute = end_datetime.minute
            
            end_time_formatted = f'{year}.{month}.{day}.T.{hour}.{minute}'
            
        
        start_time_formatted = f'{year}.{month}.{day}.T.{hour}.{minute}'
        
        filename = ""
        for name_key in name_use:
            if name_key == "use_starttime":
                filename += start_time_formatted
            else:
                meta_name = str(name_key)[4:]
                filename += trace.meta[meta_name]
                filename += "."
                
        print(filename)
        
        
        if sort_method == "starttime":
            sort_folder = start_time_formatted
        else:
            sort_folder = trace.meta[sort_method]
            
        sort_folder_path = f'{main_folder}/{sort_folder}'
        
        if not os.path.isdir(sort_folder_path):
            os.makedirs(sort_folder_path)
        
        filename = f'{station}.{channel}.{start_time_formatted}.{format}'
        
        trace.write(f'./{sort_folder_path}/{filename}')
    
        
        
       
        
        
        
        
        
        