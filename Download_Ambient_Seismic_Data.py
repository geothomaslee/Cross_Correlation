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
    """
    client_int = Client(client)
    starttime_int =  UTCDateTime(starttime)
    endtime = starttime_int + timewindow
    
    stream = client_int.get_waveforms(network, station, 
                                      location, channel, 
                                      starttime_int, endtime)
    
    return stream

test_stream = download_seismic_data(client="IRIS",
                                    starttime="2023-09-15T05:00:00.000",
                                    timewindow=3600,
                                    network="IU",
                                    station="ANMO",
                                    location="00",
                                    channel="LH?")
                                    
test_stream.plot()
