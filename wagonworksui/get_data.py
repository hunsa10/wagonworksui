# importing modules
import pandas as pd
import numpy as np

import datetime

import random

# from our utils folder
from utils import combine_datetime, get_csv_files
from utils import convert_date, xl_to_py_date, format_date
from utils import convert_time, xl_to_py_time, format_time


def get_all_data():
    '''get all data files from raw_data folder,
    transform the date cols
    merge into a single dataframe'''

    # get a list of all csv files
    csv_files = get_csv_files()

    df_list = []
    for file in csv_files:
        # read in csv file as a df
        single_df = pd.read_csv(file, low_memory = False)

        # format date columns
        single_df.loc[:,'Plan_GI_Date'] = format_date(single_df, date_col ='Plan_GI_Date')
        single_df.loc[:,'Act_GI_Date'] = format_date(single_df, date_col ='Act_GI_Date')
        single_df.loc[:,'Del_Creat_Date'] = format_date(single_df, date_col ='Del_Creat_Date')

        # format date columns
        single_df.loc[:,'Del_Creat_Time'] = format_time(single_df, time_col = 'Del_Creat_Time')


        df_list.append(single_df)


    #join the dataframes in the list together
    df = pd.concat(df_list)

    # combine date column and time column into a single datetime column
    df = combine_datetime(df)

    return df


def get_month_data(month):
    '''get the data for a single month
    in format of shortened month name, eg jan, sept'''

    # get a list of all csv files
    csv_files = get_csv_files()

    month_file = [file for file in csv_files if month.lower() in file][0]

    # read in csv file as a df
    df = pd.read_csv(month_file, low_memory = False)

    # format date columns
    df.loc[:,'Plan_GI_Date'] = format_date(df, date_col ='Plan_GI_Date')
    df.loc[:,'Act_GI_Date'] = format_date(df, date_col ='Act_GI_Date')
    df.loc[:,'Del_Creat_Date'] = format_date(df, date_col ='Del_Creat_Date')

    # format time columns
    df.loc[:,'Del_Creat_Time'] = format_time(df, time_col = 'Del_Creat_Time')

    # combine date column and time column into a single datetime column
    df = combine_datetime(df)

    return df


def get_day_data(date):
    '''get the data for a single day
    in format YYYY-MM-DD'''

    # convert date string parameter into a date
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    #extract month from date parameter
    month = str(date.month)

    # get a list of all csv files
    csv_files = get_csv_files()

    # create month dictionary to map month number to its name
    month_dict = {'1':'jan',
                  '2':'feb',
                  '3':'mar',
                  '4':'april',
                  '5':'may',
                  '6':'june',
                  '7':'july',
                  '8':'aug',
                  '9':'sept',
                  '10':'oct',
                  '11':'nov',
                  '12':'dec'}

    month_file = [file for file in csv_files if month_dict.get(month, 'missing') in file][0]

    # read in csv file as a df
    df = pd.read_csv(month_file, low_memory = False)

    # format date columns
    df.loc[:,'Plan_GI_Date'] = format_date(df, date_col ='Plan_GI_Date')
    df.loc[:,'Act_GI_Date'] = format_date(df, date_col ='Act_GI_Date')
    df.loc[:,'Del_Creat_Date'] = format_date(df, date_col ='Del_Creat_Date')

    # format time columns
    df.loc[:,'Del_Creat_Time'] = format_time(df, time_col = 'Del_Creat_Time')

    # combine date column and time column into a single datetime column
    df = combine_datetime(df)

    df = df[df['Del_Creat_DateTime'].dt.date == date]

    return df


def get_all_data_sample(days_per_month):
    '''Get data from all year
    but only get the specified sample size from each month
    days_per_month specifies the number of days to select'''
    # get a list of all csv files
    csv_files = get_csv_files()

    df_list = []
    for file in csv_files:

        # count number of rows in csv
        num_lines = sum(1 for line in open('../raw_data/ecom_testdata_june.csv'))

        # pick a sample of rows (size specified by days_per_month variable) from a the list of possible rows
        # always include the header row
        rows_to_include = [0] + random.choices(range(num_lines), k=days_per_month)

        # invert this list so it includes the rows we want to skip
        rows_to_exclude = [row for row in range(num_lines) if row not in rows_to_include]


        # read in csv file as a df
        single_df = pd.read_csv(file, low_memory = False, skiprows = rows_to_exclude, header = 0)

        # format date columns
        single_df.loc[:,'Plan_GI_Date'] = format_date(single_df, date_col ='Plan_GI_Date')
        single_df.loc[:,'Act_GI_Date'] = format_date(single_df, date_col ='Act_GI_Date')
        single_df.loc[:,'Del_Creat_Date'] = format_date(single_df, date_col ='Del_Creat_Date')

        # format date columns
        single_df.loc[:,'Del_Creat_Time'] = format_time(single_df, time_col = 'Del_Creat_Time')


        df_list.append(single_df)


    #join the dataframes in the list together
    df = pd.concat(df_list)

    # combine date column and time column into a single datetime column
    df = combine_datetime(df)

    return df
