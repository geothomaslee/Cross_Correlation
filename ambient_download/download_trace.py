# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:27:44 2023

@author: tlee4
"""

from obspy.clients.fdsn import Client
from obspy import UTCDateTime

def download_trace(client,starttime, timewindow, network, station,location, channel):
    """
    Parameters
    ----------
    client : string
        Name of Client. Defaults to IRIS. See ObsPy documentation for more.
    starttime : string
        The start time of the desired data request.
    timewindow : integer or string
        The length, in seconds, of the desired time window. It can be given
        "day" or "hour" and will automatically set the time window. If given
        a string that matches the format of starttime, it will assume this is
        the endtime.
    network : string
        Name of the network.
    station : string
        Name of the station.
    location : string
        Location code of the desired data.
    channel : string
        Channel name of the desired data.

    Returns
    -------
    stream : Obspy.Core.stream.Stream
        ObsPy stream object which should only contain one trace
    """
    client_int = Client(client)
    starttime_int =  UTCDateTime(starttime)
    
    if type(timewindow) == str:
        if timewindow == "day":
            timewindow_fin = 86400
        if timewindow == "hour":
            timewindow_fin = "3600"
        else:
            endtime = timewindow_fin
    elif type(timewindow) == int:
        endtime = starttime_int + timewindow_fin
    else:
        raise TypeError('Timewindow must be an integer or string specifying the end time')
    
    stream = client_int.get_waveforms(network, station, 
                                      location, channel, 
                                      starttime_int, endtime)
    
    return stream