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
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec
from get_data import get_month_data
import streamlit as st
from PIL import Image

# Create a page dropdown
st.sidebar.title("Site Navigation")

page = st.sidebar.selectbox("", ["Home",
                                 "Product Insights"
                                 "Warehouse Insights"])

# Create a page 'radio' - probably best to just choose one or the other
page = st.sidebar.radio("", ["Home",
                             "Business Overview",
                             "Product Insights",
                             "Warehouse Insights"])

# function for creating space between block of contents
def space():
    for i in range(3):
        st.text(' ')

# create sidebar
st.sidebar.title("Input")
select = st.sidebar.selectbox('Quantity', ['less than 10', 'bewteen 10 and 15', 'greater than 15'], key='1')
select = st.sidebar.selectbox('Product', ['Adani Green Energy', 'GMM Pfaudler', 'AGC Networks', 'Alkyl Amines Chem', 'IOL Chem & Pharma'], key='2')

st.sidebar.checkbox("Same Day Delivery")
# Separate all code for each page under their corresponding 'if' statement
if page == "Home":
    st.markdown('''
        # Wagonworks Warehouse Analysis
        ''')
    # Add a stock warehouse image
    image = Image.open('warehouse.jpg')
    st.image(image, caption='Warehouse', width=800)
    space()

    st.header("Introduction")
    st.text('some intro about the business and the project')
    space()
    space()
    st.header("Obejctives")
    st.text('-  ')
    st.text('-  ')
    st.text('-  ')

    space()
    st.header('Our Tech Stack')
    space()
    image = Image.open('../../../Downloads/tech_stack_sample.jpeg').convert('RGB')
    st.image(image, width=500)


if page == "Business Overview":

    st.header('Business Overview')
    space()
    st.button('No of orders per day: 4,377')
    st.text('')
    st.button('No of items per order: 3')
    space()
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(255, 240, 229);
        color: black;
        font-size: 20px;
        width: 500px;
        height: 50px;
    }
    </style>""", unsafe_allow_html=True)


    # orders per day graph
    st.subheader('Orders per day in 2020')
    orders_per_day = Image.open('orders per day.png')
    st.image(orders_per_day, width=1000)
    space()


if page == "Product Insights":
    # Display details of page 1
    st.markdown('''
        ## Product Insights
        ''')

    product = st.text_input('Input your product here:')

    if product:
        st.write(purchased_together('ZJBTISS52650'))


if page == "Warehouse Insights":

    st.markdown('''
    ## Warehouse Insights
    - Time per order
    - Batching vs discrete
    ''')

    st.header('Order Batching')
    uploaded_file = st.file_uploader('Order Data', type=['csv'])

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


    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown('Orders per hour')
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)


    with chart2:
        st.markdown('Average picking time')
        chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)


    st.subheader('Order Batching')
    chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

