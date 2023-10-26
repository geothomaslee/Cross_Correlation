# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:38:43 2023

@author: tlee4
"""
import os
import glob
import pandas as pd


def find_station_files(station1, station2, datafolder):
    """
    Parameters
    ----------
    station1 : string
        Name of station 1.
    station2 : string
        Name of station 2.
    datafolder : string
        Location of main data directory. ~ Will be automatically expanded to
        the home directory.

    Returns
    -------
    station1_files : list
        List of files found
    station2_files : TYPE
        List of files found.

    """
    if '~' in datafolder:
        datafolder = os.path.expanduser(datafolder)

    station1_folder = datafolder + '/' + station1
    station2_folder = datafolder + '/' + station2

    station1_files = glob.glob(f'{station1_folder}/**/*.MSEED', recursive=True)
    station2_files = glob.glob(f'{station2_folder}/**/*.MSEED', recursive=True)

    return station1_files, station2_files


def get_info_from_file_name(station1_files, station2_files, name_structure=None):
    """
    Parameters
    ----------
    station1_files : list
        List of files for station 1.
    station2_files : list
        List of files for station 2.
    name_structure : list, optional. Default is ['network','station','year','julday','hour','format'].
        A list giving the names of the data separated by periods in the name of
        the file. For example, IU.ANMO.2023.157.9.MSEED would take a list 
        ['network','station','year','julday','hour','format']. This is also the
        default file structure assumed if none is given.

    Returns
    -------
    station1_df : pandas.DataFrame
        DataFrame containing the information pulled from the file name for station 1.
    station2_df : TYPE
        DataFrame containing the information pulled from the file name for station 2.

    """
    if name_structure == None:
        name_structure = ['network', 'station',
                          'year', 'julday', 'hour', 'format']

    if len(station1_files) != len(station2_files):
        raise ValueError(
            'Station 1 has a different number of windows than Station 2')

    # Pull the name of the file structure and break it down into its information
    file_name_structure = station1_files[-1].split(
        '/')[-1].split('\\')[-1].split('.')

    if len(file_name_structure) != len(name_structure):
        raise ValueError(
            'Name structure of found files does not match given name structure')

    # Create the column index list and an empty list for inputting data
    df_index = name_structure.copy()
    df_index.append("file")
    all_data_list = []

    for i, file in enumerate(station1_files):
        int_data_list = []
        file_name_structure = file.split('/')[-1].split('\\')[-1].split('.')

        for i in range(len(name_structure)):
            data_add = file_name_structure[i]
            int_data_list.append(data_add)

        # Pulls important info for each file and puts it into a DataFrame
        int_data_list.append(file)

        all_data_list.append(int_data_list)

    station1_df = pd.DataFrame(all_data_list, columns=df_index)

    # Separator comment for legibility

    all_data_list = []

    for i, file in enumerate(station2_files):
        int_data_list = []
        file_name_structure = file.split('/')[-1].split('\\')[-1].split('.')

        for i in range(len(name_structure)):
            data_add = file_name_structure[i]
            int_data_list.append(data_add)

        # Pulls important info for each file and puts it into a DataFrame
        int_data_list.append(file)

        all_data_list.append(int_data_list)

    # Creates the DataFrame for the stations
    station2_df = pd.DataFrame(all_data_list, columns=df_index)

    return station1_df, station2_df


def compare_files(station1_df, station2_df, different='station'):

    # Checking the type for different. Assumed to be a list, if a string is given
    # then it will be turned into a list of length 1.

    if different == None:
        raise ValueError(
            'The name of the information that should be different must be given')
    elif type(different) == str:
        different_list = [different]
    elif type(different) == list:
        different_list = different.copy()
    else:
        raise ValueError('Different must be a list')

    # Checks to see that every item in different_list is a string
    if all(isinstance(item, str) for item in different_list):
        pass
    else:
        raise TypeError('Items in different list must be strings')
   
    
   
    
   
    
station1_files, station2_files = find_station_files(
    'ANMO', 'TUC', '~/Documents/Correlation_Testing_Data')

df1, df2 = get_info_from_file_name(
    station1_files, station2_files, name_structure=None)

compare_files(df1, df2)
