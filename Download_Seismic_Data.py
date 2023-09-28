# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:27:44 2023

@author: tlee4
"""

from obspy.clients.fdsn import Client
from obspy import UTCDateTime

def download_seismic_data(client, starttime, timewindow, network, station, location, channel):
    """
    client: string containing the name of the client - most likely IRIS. See
    obspy.clients.fdsn documentation for more potential client sources
    
    starttime: string giving the starttime of the requested data, in the format
    year-mm-ddThr-mn-sc.000
    
    timewindow = integer giving the length of the time window in seconds.
    
    network: string containing the network name. Ex. "IU"
    
    station: string containing station name. Ex. "ANMO"
    
    location: string containing location. Usually, "00"
    
    channel: string containing channel name. This can be globbed to look for
    all channels, or specific channels.
    Ex. "*" for all channels
    Ex."B*" for all channels starting with B
    Ex. "BH?" for all components starting with BH
    Ex. "?HZ" for vertical component when unsure of the channel name convention
    ---------
    Returns: stream, an obspy.core.stream.Stream object
    
    See obspy.core.stream.Stream documentation for more info on how to work
    with stream objects
    ---------
    This is best for when dealing with smaller amounts of data, but can be
    needlessly cumbersome on the servers when dealing with a lot of separate
    requests. See bulk_download_seismic_data for when dealing with a lot of
    data that is coming in many different requests
    ---------
    """
    client_int = Client(client)
    starttime_int =  UTCDateTime(starttime)
    endtime = starttime_int + timewindow
    
    stream = client_int.get_waveforms(network, station, 
                                      location, channel, 
                                      starttime_int, endtime)
    
    return stream

# Plotting up a quick example to show how the script works
example_stream = download_seismic_data(client="IRIS",
                                       starttime="2023-09-15T05:00:00.000",
                                       timewindow=3600,
                                       network="IU",
                                       station="ANMO",
                                       location="00",
                                       channel="LH?")
                                    
example_stream.plot()

def bulk_download_seismic_data(client, starttime, timewindow, network, station, location, channel):
    """
    client: list of strings giving the name of the client - most likely IRIS. 
    See obspy.clients.fdsn documentation for more potential client sources
    
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
    This is best for when dealing with smaller amounts of data, but can be
    needlessly cumbersome on the servers when dealing with a lot of separate
    requests. See bulk_download_seismic_data for when dealing with a lot of
    data that is coming in many different requests
    """
    
    arguments = locals()
    print(arguments)
    
    ""
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
    
    # For items inputted not as a list, we need to assume that we just want to
    # use that value for every trace. This creates a list with the same length
    # as the list variables for which every entry is the non-list input
    
    arg_dict = {}
    for non_list_arg in non_list_args:
        temp_list = []
        for i in range(base_len):
            temp_list.append(non_list_arg)
        
        arg_dict[non_list_arg] = []
        arg_dict[non_list_arg].append(temp_list)
        
    for list_arg in list_args_keys:
        arg_dict[list_arg] = []
        arg_dict[list_arg].append(arguments[list_arg])
        
        
    client_int = Client(client)
    starttime_int =  UTCDateTime(starttime)
    endtime = starttime_int + timewindow
    
    print(arg_dict)
    
    """
    stream = client_int.get_waveforms_bulk(network=network_list, 
                                           station=station_list, 
                                           location=location_list, 
                                           channel=channel_list, 
                                           starttime_int=starttime_int_list, 
                                           endtime_list)
    
    return stream
    """

client_list = ["IRIS", "IRIS"]
network_list = ["IU", "IU"]

example_bulk_stream = bulk_download_seismic_data(client=client_list,
                                                  starttime="2023-09-15T05:00:00.000",
                                                  timewindow=3600,
                                                  network=network_list,
                                                  station="ANMO",
                                                  location="00",
                                                  channel="LH?")
                                    
example_bulk_stream.plot()
    