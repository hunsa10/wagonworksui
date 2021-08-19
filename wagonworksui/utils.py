# importing module
import os
import pandas as pd
import numpy as np

import datetime

# File utility functions

def get_csv_files():
    # Get the list of all files in raw_data
    all_files = [f'raw_data/{file}' for file in os.listdir("raw_data")]

    # filter for csv files
    csv_files = [file.lower() for file in all_files if (file[-3:] == "csv")]
    return csv_files

# Date utility functions

def convert_date(days):
    '''convert a excel date (number of days from 1900-01-01) into a python time'''
    # set excels base date
    base_date = datetime.datetime(1899, 12, 30)
    # calculate number of days since base date
    py_date = base_date + datetime.timedelta(days = days)
    return py_date

def xl_to_py_date(df, col = False):
    '''apply our xl to py date conversion function'''
    if bool(col):
        df = df.dropna(subset=[col])
        df.loc[:,col] = df.loc[:,col].apply(lambda row: convert_date(row))
    return df

def format_date(df, date_col):
    '''format the date column depending on its original type'''
    # check type of date column
    date_type = df.loc[:,date_col].dtype

    # convert to date type depending on its original type
    if date_type == object:
        df.loc[:,date_col] = pd.to_datetime(df.loc[:,date_col]).dt.normalize()

    if date_type == int or date_type == float:
        df.loc[:,date_col] = xl_to_py_date(df, col = date_col)

    return df.loc[:,date_col]



# Time utility functions

def convert_time(days):
    '''convert a excel time (proportion of the way through the day) into a python time'''
    # convert to number of seconds
    xl_seconds = int(days * 24 * 3600)
    # calculate hours, minutes, and seconds
    py_time = datetime.time(xl_seconds//3600, (xl_seconds%3600)//60, xl_seconds%60)
    return py_time


def xl_to_py_time(df, col = False):
    '''apply our xl to py time conversion function'''
    if bool(col):
        df = df.dropna(subset=[col])
        df.loc[:,col] = df.loc[:,col].apply(lambda row: convert_time(row))
    return df

def format_time(df, time_col):
    '''format the time column depending on its original type'''
    # check type of time column
    time_type = df.loc[:,time_col].dtype

    # convert to date type depending on its original type
    if time_type == object:
        df.loc[:,time_col] = pd.to_datetime(df.loc[:,time_col], format='%I:%M:%S %p').dt.time

    if time_type == int or time_type == float:
        df.loc[:,time_col] = xl_to_py_time(df, col = time_col)

    return df.loc[:,time_col]

# combining a date time column

def combine_datetime(df):
    '''combine date and time columns into a single datetime column'''

    df.loc[:,'Del_Creat_DateTime'] = pd.to_datetime(df.loc[:,'Del_Creat_Date'].astype(str) + ' ' + df.loc[:,'Del_Creat_Time'].astype(str), errors = 'coerce')

    return df
