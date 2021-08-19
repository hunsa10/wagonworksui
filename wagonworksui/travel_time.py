# Import modules
import pandas as pd
import datetime
from wagonworks.get_data import get_day_data


# Process time should beinput arguments
process_tasks_time = {'scan_time': 3,
                      'confirm_location': 2,
                      'pick_time': 8,
                      'confirm_pick': 2,
                      'confirm_box': 5}


def discrete_time(order_df, process_tasks_time):
    '''
    This function calculates the total time to complete all given orders using
    discrete picking method.
    Input is:
    - order_df: a dataframe containing all the order IDs and corresponding SKU
    IDs to be
        completed. (Possibly recommend orders in one hour)
    - process_tasks_time: a dictionary containing the process tasks per order
    and their average time.

    Output is:
    - Dataframe with:
        - Del_Number: Order ID
        - Discrete_travel_time: the return travel time per order
        - Discrete_total_order_time: the total time per order (travel time and
        process time)
    - The total time to complete all orders (in days/hours)
    '''

    # Get sku_location_time reference table which gives a one-way travel time
    # for each location zone and SKU
    sku_location_time_df = pd.read_csv(
                            '../raw_data/reference_data/sku_location_time.csv')

    # Merge order_df and sku_location_time_df to get the average travel time
    # for each SKU
    order_merge_df = order_df.merge(sku_location_time_df,
                                    how='left',
                                    on='SKU',
                                    copy=False)

    # Group together by order number to get the total travel time per order
    order_grouped_df = order_merge_df.groupby('Del_Number').sum('TIME') * 2

    # Calculate total order time (adding on process time)
    order_grouped_df['Discrete_total_order_time'] = \
        order_grouped_df['TIME'] + sum(process_tasks_time.values())

    # Keep only time columns
    order_grouped_df = order_grouped_df[['TIME', 'Discrete_total_order_time']]

    # Change column names
    order_grouped_df.columns = ['Discrete_travel_time',
                                'Discrete_total_order_time']

    # Convert seconds to hh:mm:ss format
    total_time_sec = int(order_grouped_df['Discrete_total_order_time'].sum())
    total_time = str(datetime.timedelta(seconds=total_time_sec))

    # Return the total time it takes to complete all orders
    return order_grouped_df, total_time


def batch_time(order_df, batch_df, process_tasks_time, sort_time=20):
    '''
    Input is:
    - order_df: a dataframe containing all the order IDs and corresponding SKU
    IDs to be completed.
    - batch_df: a dataframe containing all the order IDs and corresponding
    batch IDs from batching analysis.
    - sku_location_time_df: a reference dataframe containing all unique
    possible SKU IDs with their corresponding location zone and average one-way
    travel time.
    - sort_time: time it takes to sort each SKU in a batch
    - process_tasks_time: a dictionary containing the process tasks per order
    and their average time.
    Output is:
    - Dataframe with:
        - Batch_Number
        - Total_batch_time: time per batch + process time per batch
    - The total time to complete all orders (in days/hours)
    '''

    # Get sku_location_time reference table which gives a one-way travel time
    # for each location zone and SKU
    sku_location_time_df = \
        pd.read_csv('../raw_data/reference_data/sku_location_time.csv')

    # Merge order_df and batch_df so that we can associate batch and SKU IDs
    order_merged_df = order_df.merge(batch_df,
                                     how='left',
                                     on='Del_Number',
                                     copy=False)

    # Separate SKU-dependent process tasks and order-dependent process tasks:
    # Scan time is incorporated into sorting time for batches so is no longer
    # included in this step, confirm location, pick time and confirm pick all
    # happen once per SKU in a batch finally, confirm box will happen once per
    # order
    SKU_keys = ['confirm_location', 'pick_time', 'confirm_pick']
    SKU_process_time = {key: process_tasks_time[key] for key in SKU_keys}
    order_process_time = process_tasks_time['confirm_box']

    # Calculate time per batch
    # Get number of batches for loop range
    max_batch = order_merged_df['Batch_Number'].max()

    # Create empty dataframe to fill
    batch_time_df = pd.DataFrame({'Batch_Number': [],
                                  'Batch_Time': []}, dtype=int)

    for batch in range(max_batch + 1):
        # Get all unique SKUs in each batch
        batch_grouped_df = \
                        pd.DataFrame(
                            order_merged_df[order_merged_df['Batch_Number'] == batch]['SKU'].unique())
        batch_grouped_df.columns = ['SKU']

        # Merge SKUs list with sku_location_time_df
        batch_SKUs_merged_df = \
            batch_grouped_df.merge(sku_location_time_df,
                                   how='left',
                                   on='SKU',
                                   copy=False).drop('SKU LOCATION', axis=1)

        # Add a column with total time per SKU in the batch
        batch_SKUs_merged_df['total_SKU_time'] = batch_SKUs_merged_df['TIME'] \
            * 2 + sort_time

        # Drop time column
        batch_SKUs_merged_df = batch_SKUs_merged_df.drop('TIME', axis=1)

        # Create a dataframe with Batch_Number and time
        # First get number of orders in the batch to multiply by order process
        # task time
        n_orders = len(
            order_merged_df[order_merged_df['Batch_Number'] == batch].groupby(
                'Del_Number').count())
        process_time = sum(SKU_process_time.values()) + order_process_time * \
            n_orders
        batch_time = batch_SKUs_merged_df['total_SKU_time'].sum() + \
            process_time
        batch_time_df.loc[batch, ['Batch_Number', 'Batch_Time']] = \
            [batch, batch_time]

        # Convert seconds to hh:mm:ss format
        total_time_sec = int(batch_time_df['Batch_Time'].sum())
        total_time = str(datetime.timedelta(seconds=total_time_sec))

    # Convert final dataframe to int
    batch_time_df = batch_time_df.astype(int)

    return batch_time_df, total_time

