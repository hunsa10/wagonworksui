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

# Create a page dropdown
st.sidebar.title("Menu")

# page = st.sidebar.selectbox("", ["Home",
#                                  "Product Insights"
#                                  "Warehouse Insights"])

# Create a page 'radio' - probably best to just choose one or the other
page = st.sidebar.radio("", ["Home",
                             #"Business Overview",
                             "Warehouse Insights",
                             "Product Insights"])

# function for creating space between block of contents
def space():
    for i in range(3):
        st.text(' ')

# create sidebar
# st.sidebar.title("Input")
# select = st.sidebar.selectbox('Quantity', ['less than 10', 'bewteen 10 and 15', 'greater than 15'], key='1')
# select = st.sidebar.selectbox('Product', ['Adani Green Energy', 'GMM Pfaudler', 'AGC Networks', 'Alkyl Amines Chem', 'IOL Chem & Pharma'], key='2')

# Separate all code for each page under their corresponding 'if' statement
if page == "Home":
    st.markdown('''
        # E-Commerce Warehouse Analysis
        ''')
    st.markdown('''
    Organise your orders efficiently for the day!
    - Find out which items customers often buy together
    - Get lists of your orders for most efficient picking
    ''')
    # Add a stock warehouse image
    # image = Image.open('warehouse.jpg')
    # st.image(image, width=400)
    #space()


# if page == "Business Overview":

#     st.header('Business Overview')
#     space()
#     st.button('No of orders per day: 4,377')
#     st.text('')
#     st.button('No of items per order: 3')
#     space()
#     m = st.markdown("""
#     <style>
#     div.stButton > button:first-child {
#         background-color: rgb(255, 240, 229);
#         color: black;
#         font-size: 20px;
#         width: 500px;
#         height: 50px;
#     }
#     </style>""", unsafe_allow_html=True)


    # orders per day graph
    # st.subheader('Orders per day in 2020')
    # orders_per_day = Image.open('orders per day.png')
    # st.image(orders_per_day, width=1000)
    # space()


if page == "Warehouse Insights":

    st.header('Order Batching')

    st.header("Step 1: Upload orders for the day")
    # st.text('some intro about the business and the project')
    uploaded_file = st.file_uploader('Order Data', type=['csv'])
    space()

    if uploaded_file:
        order_pool_ui(uploaded_file)

    st.header('Step 2: Choose parameters')

    st.markdown('Priority Flag')
    option = st.selectbox('Same day delivery', ['Same day', 'Next day',
                                                'All'])

    st.markdown('Estimated processing times (in seconds)')

    col1, col2 = st.beta_columns(2)
    with col1:
        scan_time = st.text_input('Scan time', 3)
        confirm_location = st.text_input('Confirm location time', 2)
        pick_time = st.text_input('Pick time', 8)

    with col2:
        confirm_pick = st.text_input('Confirm pick time', 2)
        confirm_box = st.text_input('Confirm box time', 5)
        sort_time = st.text_input('Sort time per SKU', 20)

    st.header('Step 3: Run')
    # if st.button('Process orders'):
    #     # batch_function(uploaded_file)
    # space()
    # space()

if page == "Product Insights":
    # Display details of page 1
    st.markdown('''
        ## Product Insights
        ''')

    st.header("Step 1: Upload the dataset")
        # st.text('some intro about the business and the project')
    uploaded_file = st.file_uploader('Order Data', type=['csv'])
    space()
    st.header('Step 2: Choose parameters')

    product = st.text_input('Input your product here:')

    if product:
        st.write(purchased_together('ZJBTISS52650'))

    # st.markdown('Priority Flag')
    # option = st.selectbox('Same day delivery', ['Same day', 'Next day',
                                                # 'All'])

    # st.markdown('Estimated processing times (in seconds)')

    # col1, col2 = st.beta_columns(2)
    # with col1:
    #     scan_time = st.text_input('Scan time', 3)
    #     confirm_location = st.text_input('Confirm location time', 2)
    #     pick_time = st.text_input('Pick time', 8)

    # with col2:
    #     confirm_pick = st.text_input('Confirm pick time', 2)
    #     confirm_box = st.text_input('Confirm box time', 5)
    #     sort_time = st.text_input('Sort time per SKU', 20)

    st.header('Step 3: Run')
    # if st.button('Process orders'):
    #     # batch_function(uploaded_file)
    # space()
    # space(
    # st.header('Business Overview')
    # space()
    # st.button('No of orders per day: 4,377')
    # st.text('')
    # st.button('No of items per order: 3')
    # space()
    # m = st.markdown("""
    # <style>
    # div.stButton > button:first-child {
    #     background-color: rgb(255, 240, 229);
    #     color: black;
    #     font-size: 20px;
    #     width: 500px;
    #     height: 50px;
    # }
    # </style>""", unsafe_allow_html=True)
    # space()


    # uploaded_file = st.file_uploader('Order Data', type=['csv'])

    #if uploaded_file:
        # action

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


    # Examples
    df = pd.DataFrame({'x': list(range(10)), 'y': list(range(10))})
    st.write(df)

    if st.button('Download Dataframe as CSV'):
      tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
      st.markdown(tmp_download_link, unsafe_allow_html=True)

    st.header('Demonstration')

    df = pd.read_csv('raw_data/centroid_df.csv')

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


    # chart1, chart2 = st.columns(2)

    # with chart1:
    #     st.markdown('Orders per hour')
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.line_chart(chart_data)


    # with chart2:
    #     st.markdown('Average picking time')
    #     chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    #     st.line_chart(chart_data)


    # st.subheader('Order Batching')
    # chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    # st.line_chart(chart_data)

