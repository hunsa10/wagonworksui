import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from affinity_analysis import purchased_together
from PIL import Image
import base64
import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
# from tensorflow.keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec
# from get_data import get_month_data
import streamlit as st
from wagonworksui.order_pool import order_pool_ui
import requests

#changing app name and icon
img = Image.open('download.jpg')
st.set_page_config(page_title='Warehouse App', page_icon=img)


# Create a page dropdown
st.sidebar.title("Menu")

# Create a page 'radio' - probably best to just choose one or the other
page = st.sidebar.radio("", ["Home",
                             "Warehouse Insights",
                             "Product Insights"])

# defining functions for the app:
def big_space():
    for i in range(3):
        st.text(' ')

def small_space():
    for i in range(1):
        st.text(' ')

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

        # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


# Separate all code for each page under their corresponding 'if' statement
if page == "Home":
    st.markdown('''
        # E-Commerce Warehouse Optimization
        ''')
    big_space()
    st.markdown('''
    Organise your orders efficiently for the day!
    - Get lists of your orders for most efficient picking
    - Find out which items customers often buy together
    ''')
    big_space()
    img2 = Image.open("image_ware.jpg")
    st.image(img2)

#upload warehouse orders and get the pool

if page == "Warehouse Insights":

    st.title('Order Batching')
    st.markdown('''
    Get lists of your orders for most efficient picking
    ''')
    big_space()
    st.subheader("Step 1: Upload orders for the day")
    small_space()
    uploaded_file = st.file_uploader('Orders Data', type=['csv'])
    small_space()

    # if st.button('Data Preview'):
    #     data_preview = pd.DataFrame(uploaded_file)
    #     st.write(data_preview.head())
    #     small_space()
    # choose parameters to order batching

    st.subheader('Step 2: Choose parameters')
    small_space()
    st.markdown('Priority Flag')
    option = st.selectbox('Same day delivery', ['Same day', 'Next day',
                                                'All'])

    if option != 'Same day':
        small_space()
        st.markdown('Choose hour of the day for orders to process (from 6am to 11pm)')
        hour = int(st.text_input('Hour (between 6 - 23)', 6))

    small_space()
    st.markdown('Estimated processing times (in seconds)')

    col1, col2 = st.columns(2)
    with col1:
        scan_time = st.text_input('Scan time', 3)
        confirm_location = st.text_input('Confirm location time', 2)
        pick_time = st.text_input('Pick time', 8)

    with col2:
        confirm_pick = st.text_input('Confirm pick time', 2)
        confirm_box = st.text_input('Confirm box time', 5)
        sort_time = st.text_input('Sort time per SKU', 10)

    # Run the batching model

    st.subheader('Step 3: Run the model')
    small_space()
    if st.button('Run'):
        small_space()

        if uploaded_file:

            # uploaded_file_df = pd.read_csv(uploaded_file)
            if option == 'Same day':
                pool_result = order_pool_ui(uploaded_file, same_day=True)[0]
            elif option == 'Next day':
                pool_result = order_pool_ui(uploaded_file, next_day=True)[hour-6]
            else:
                pool_result = order_pool_ui(uploaded_file)[hour-6]


            # convert data into a list of dictionaries

            # ADD LOOP TO GO THROUGH ALL DATAFRAMES

            data_dict= pool_result.to_dict(orient='records')

            api_url = f'https://wagonworks-api-dsvsmf3mja-de.a.run.app/warehouse?sort_time={sort_time}&scan_time={scan_time}&confirm_location={confirm_location}&pick_time={pick_time}&confirm_pick={confirm_pick}&confirm_box={confirm_box}'

            response = requests.post(api_url, json=data_dict).json()

            if response['Fastest_method'] != 'discrete':

                st.write(f'Time saved is {round(- response["Time_saved"]/60)} minutes')

                st.write(f"Hybrid picking was the fastest method found taking \
                {response['Best_time_result'] // (60*60)} hour(s) and {round(response['Best_time_result'] % (60*60) / 60)} minutes")

            else:
                st.write(f"{response['Fastest_method'].capitalize()} picking was the fastest method found taking\
                {response['Best_time_result'] // (60*60)} hour(s) and {round(response['Best_time_result'] % (60*60) / 60)} minutes")

            dollar_input = 40
            st.write(f"This is a cost of ${round(response['Best_time_result'] * 0.01111111111111111, 2)} at ${str(dollar_input)} an hour")

            batch_labels = pd.DataFrame(response['Order_labels'])

            # show csv to be downloaded
            tmp_download_link = download_link(batch_labels, 'batching_result.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

        else:
            st.write("Please upload a csv file")

# Product insights model

if page == "Product Insights":
    # Display details of page 1
    st.title('Product Insights')
    st.markdown('''
    Find out which items customers often buy together
    ''')
    big_space()

    #product groups
    st.header('Product clusters')
    small_space()
    st.subheader("Step 1: Upload the dataset")
        # st.text('some intro about the business and the project')
    uploaded_file = st.file_uploader('Order Data', type=['csv'])

    # if st.button('Data Preview'):
    #     data_preview = pd.DataFrame(uploaded_file)
    #     st.write(data_preview.head())

    small_space()
    st.subheader('Step 2: Analyse groups of products')

    if st.button('Graph'):
        small_space()

        df = pd.read_csv('data/centroid_df.csv')

        fig = px.scatter(df, x='x', y='y', size='Size',
                         color='Group',
                         #symbol_map=[1, 2, 3, 4],
                         hover_name="Grouped Items",
                         hover_data={'Grouped Items': False,
                                     'y': False,
                                    'Group': False,
                                    'Size': False},
                         log_x=False,
                         size_max=80,
                         labels={'x': '', 'y': ''},
                         title="Top 5 groups of items repeatedly bought together")

        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Helvetica"
                )
            )
        st.plotly_chart(fig, use_container_width=True)

    # else:
    #     st.write("Please upload a csv file")

    #Products frequently bought together per sku
    big_space()
    st.header('Products purchased together per SKU')
    small_space()
    st.subheader('Step 1: Choose a SKU')

    product = st.text_input('Input the SKU of your product here:')

    small_space()
    st.subheader('Step 2: Show list of SKUs')

    if st.button('List'):
        product_df = pd.DataFrame({'Product_SKU': ['ZBI13AS39932',
                                       'ZST3WP444007',
                                       'ZSPQ12R42525',
                                       'ZEN900034005',
                                       'ZJBR0A454225',
                                       'ZSM41BE13555',
                                       'ZJBCPE24843',
                                       'ZES55KT15592',
                                       'ZEN90006816',
                                       'ZMEGSTA50658'] })
        st.write(product_df)

# show csv to be downloaded
        tmp_download_link = download_link(product_df, 'product_df.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
