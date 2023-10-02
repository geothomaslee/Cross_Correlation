# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:40:27 2023

@author: tlee4
"""

from ambient_download.bulk_seis_download import bulk_download_seismic_data
#from ambient_download.seis_download import download_seismic_data
from ambient_download.get_ambient_times import get_ambient_windows
from ambient_download.save_stream import save_stream_traces


starttime = "2023-09-27T00:00:00.000"
window_length = 60
total_time =  180

starttimes, endtimes = get_ambient_windows(starttime, window_length, total_time, 1)


ambient_stream = bulk_download_seismic_data(client="IRIS",
                                            starttime=starttimes,
                                            endtime=endtimes,
                                            network="IU",
                                            station="ANMO",
                                            location="00",
                                            channel="LHZ")

print(ambient_stream)

save_stream_traces(stream=ambient_stream, sort_method="station",
                   force_overwrite=True)
    