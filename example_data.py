# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 21:41:44 2023

@author: tlee4
"""

from ambient_download.bulk_seis_download import bulk_download_seismic_data
from ambient_download.seis_download import download_seismic_data
from ambient_download.get_ambient_times import get_ambient_windows
#from ambient_download.save_stream import save_stream_traces

starttime = "2023-02-06T01:17:00.000"
endtime = "2023-02-06T01:45:00.000"

station_list = ['ANTO','PAB','SSPA','CCM','ANMO']

"""
eq_stream = bulk_download_seismic_data(client="IRIS",
                                       starttime=starttime,
                                       endtime=endtime,
                                       network="IU",
                                       station=station_list,
                                       location="00",
                                       channel="BHZ")

eq_stream.plot(equal_scale=False)
"""

starttime = "2011-03-11T05:46:00.000"
endtime = "2011-03-11T07:00:00.000"

channel_list = ["BH1","BH2","BHZ"]

Japan_Stream = bulk_download_seismic_data(client="IRIS",
                                          starttime=starttime,
                                          endtime=endtime,
                                          network="IU",
                                          station="ANMO",
                                          location="00",
                                          channel=channel_list)
Japan_Stream.plot()
Japan_Stream[2].plot()
print(Japan_Stream[1].meta)
