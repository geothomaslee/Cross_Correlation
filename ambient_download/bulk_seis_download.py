# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:26:46 2023

@author: tlee4
"""
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import pandas as pd

def bulk_download_seismic_data(client, starttime, endtime, network, station, location, channel):
    """
    client: string giving the name of the client - most likely IRIS. 
    See obspy.clients.fdsn documentation for more potential client sources.
    Note that only ONE client can be used per request. Datasets involving
    separate clients must be downloaded in separate requests.
    
    starttime: list of strings giving the starttime of the requested data, in 
    the format year-mm-ddThr-mn-sc.000
    
    timewindow = list of integers giving the length of required time in seconds
    
    network: list of strings giving the network name. Ex. "IU"
    
    station: list of strings giving station name. Ex. "ANMO"
    
    location: list of strings giving location. Usually, "00"
    
    channel: lust of strings containing channel name. This can be globbed to 
    look for all channels, or specific channels.
    Ex. "*" for all channels
    Ex."B*" for all channels starting with B
    Ex. "BH?" for all components starting with BH
    Ex. "?HZ" for vertical component when unsure of the channel name convention
    
    NOTE: can feed a string instead of a list to client, and it will assume
    that every requested trace has the same client
    ---------
    Returns: stream, an obspy.core.stream.Stream object containing all the
    requested traces
    
    See obspy.core.stream.Stream documentation for more info on how to work
    with stream objects
    ---------
    If you are downloading continuous data and are requesting separate, but 
    consecutive, time windows, this module will combine all of them into one
    trace. Thus, its use is somewhat limited for things like ambient noise
    where you may want to download your correlation windows already cut instead
    of cutting them yourself. However, it is still useful for many other
    applications of downloading data.
    """
    
    arguments = locals()
    
    # Checks to see if any lists have been inputted
    list_args = []
    list_args_keys = []
    non_list_args = []
    for arg, arg_values in arguments.items():
        arg_type = type(arg_values)
        if arg_type == list:
            list_args.append(arg_values)
            list_args_keys.append(arg)
        else:
            non_list_args.append(arg)
            
    # Raises an error if no lists have been inputted
    if not list_args:
        raise TypeError("At least one input must be a list. Use download_seismic_data for single traces")
    
    # Checks if lists are longer than one and have the same length
    base_len = len(list_args[0])
    for arg in list_args:
        if len(arg) != base_len:
            raise ValueError("Input lists must have the same length")
        if len(arg) <= 1:
            raise ValueError("Lists must have length greater than 1 for bulk download")
    
    # Checks if more than one client has been fed into client
    if type(arguments["client"]) != str:
        raise TypeError('Client must be a string and can only handle one client per request')
        
    
    # For items inputted not as a list, we need to assume that we just want to
    # use that value for every trace. This creates a list with the same length
    # as the list variables for which every entry is the non-list input
    arg_dict = {}
    for non_list_arg in non_list_args:
        temp_list = []
        for i in range(base_len):
            temp_list.append(arguments[non_list_arg])
       
        arg_dict[non_list_arg] = temp_list
        
    # Putting the actual list variables into our new argument dictionary for
    # The sake of consistency    
    for list_arg_key in list_args_keys:
        arg_dict[list_arg_key] = arguments[list_arg_key]
    
    UTC_Start_Time_List = []
    for time in arg_dict['starttime']:
        UTC_Start_Time = UTCDateTime(time)
        UTC_Start_Time_List.append(UTC_Start_Time)
    
    UTC_End_Time_List = []
    for time in arg_dict['endtime']:
        UTC_End_Time = UTCDateTime(time)
        UTC_End_Time_List.append(UTC_End_Time)
        
    arg_dict['starttime'] = UTC_Start_Time_List
    arg_dict['endtime'] = UTC_End_Time_List
    
    
    # Client shouldn't be a list so doing this is easiest fix
    arg_dict['client'] = arguments['client']
        
    # Creating our internal client
    client_int = Client(arg_dict['client'])
    
    
    # Turns our arg dictionary into a Pandas dataframe because this makes
    # re-ordering the thing easier... I think? Honestly not sure this is most 
    # efficient but it's what I'm going to do
    
    arg_df = pd.DataFrame.from_dict(arg_dict)
    arg_df = arg_df.drop(columns=['client'])
    
    bulk_list_names = ['network','station','location','channel','starttime','endtime']
    bulk_list_order = []
    for arg in bulk_list_names:
        pos = arg_df.columns.get_loc(arg)
        bulk_list_order.append(pos)
    
    arg_df = arg_df.iloc[:,bulk_list_order]
    
    # obspy.clients.fdsn.client.Client.get_waveforms_bulk() takes a list of
    # lists called the bulk, wherein each value of the main bulk list is an 
    # ordered list of the input parameters for each individual request
    
    bulk = []
    for i in range(len(arg_df.index)):
        row = arg_df.loc[i,:].values.flatten().tolist()
        bulk.append(row)
        
        stream = client_int.get_waveforms_bulk(bulk)
    
    return stream