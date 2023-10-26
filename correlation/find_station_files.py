# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:38:43 2023

@author: tlee4
"""
import os
import glob

def find_station_files(station1, station2, datafolder):
    station1_folder = datafolder + '/' + station1
     
    print(station1_folder)
    files = glob.glob(f'{station1_folder}/**/*.MSEED', recursive=True)
    
    print(files)
    
find_station_files('ANMO','TUC','~/Documents/Correlation_Testing_Data')