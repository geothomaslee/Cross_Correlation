# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:38:43 2023

@author: tlee4
"""
import os
import glob

def find_station_files(station1, station2, datafolder,name_structure=None):
    if '~' in datafolder:
        datafolder = os.path.expanduser(datafolder)
    
    station1_folder = datafolder + '/' + station1
    station2_folder = datafolder + '/' + station2
    
    station1_files = glob.glob(f'{station1_folder}/**/*.MSEED', recursive=True)
    station2_files = glob.glob(f'{station2_folder}/**/*.MSEED', recursive=True)
    
    return station1_files, station2_files

def get_file_name_meta(station1_files,station2_files,name_structure=None):
    if name_structure == None:
        name_structure = ['network','station','year','julday','9','MSEED']
        
    if len(station1_files) != len(station2_files):
        raise ValueError('Station 1 has a different number of windows than Station 2')

    # Pull the name of the file structure and break it down into its information
    file_name_structure = station1_files[-1].split('/')[-1].split('\\')[-1].split('.')
    
    if len(file_name_structure) != len(name_structure):
        raise ValueError('Name structure of found files does not match given name structure')



station1_files, station2_files = find_station_files('ANMO','TUC','~/Documents/Correlation_Testing_Data')
                                                    