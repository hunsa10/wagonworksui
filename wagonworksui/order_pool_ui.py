# importing modules
import pandas as pd
import numpy as np
import datetime
from wagonworks.utils import format_date, format_time


def order_pool_ui(csv):
    '''Get all the orders of a day and prioritize the ones with same_day flag,
    the output is a list of dataframes with new orders per hour and the following
    columns Del_order, SKU and quantity of items per order, datetime and same_day_flag
    Assumption: the OW system will stop to send orders with same_day flags by
    11am.'''

    # read in csv file as a df
    single_df = pd.read_csv(csv, low_memory = False)

    # format date columns
    single_df.loc[:,'Plan_GI_Date'] = format_date(single_df, date_col ='Plan_GI_Date')
    single_df.loc[:,'Act_GI_Date'] = format_date(single_df, date_col ='Act_GI_Date')
    single_df.loc[:,'Del_Creat_Date'] = format_date(single_df, date_col ='Del_Creat_Date')

    # format date columns
    single_df.loc[:,'Del_Creat_Time'] = format_time(single_df, time_col = 'Del_Creat_Time')

    # creating a loop vgariable to drop done orders
    loop_dataframe = single_df.copy()
    orders_list = []

    while len(loop_dataframe) > 0:

        #condition to prioritise same day orders
        if len(loop_dataframe[loop_dataframe['Same_Day_Flag'] == 'X']) > 0:
            day_flag = loop_dataframe[loop_dataframe['Same_Day_Flag'] == 'X'][['Del_NumA','SKU_A','Act_Goods_Issue_Qty_SKU','Del_Creat_DateTime', 'Same_Day_Flag']]
        else:
            day_flag = loop_dataframe[loop_dataframe['Same_Day_Flag'] != 'X'][['Del_NumA','SKU_A','Act_Goods_Issue_Qty_SKU','Del_Creat_DateTime', 'Same_Day_Flag']]

        #select orders of the first available hour
        day_flag['Hour'] = day_flag['Del_Creat_DateTime'].dt.hour
        orders_time = day_flag['Hour'].min()
        hour_df = day_flag[day_flag['Hour'] == orders_time]
        hour_df_index = day_flag[day_flag['Hour'] == orders_time].index

        #create list of dataframes to be sent to batch
        loop_dataframe.drop(hour_df_index, axis = 0, inplace = True)
        hour_df.reset_index(drop = True, inplace = True)
        hour_df.rename(columns={'SKU_A':'SKU', 'Del_NumA': 'Del_Number'}, inplace=True)
        orders_list.append(hour_df)

    return orders_list
