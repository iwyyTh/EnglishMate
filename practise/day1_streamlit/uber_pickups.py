import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('loading data ...')

data = load_data(100000)

data_load_state.text('Done! (using st.cache_data)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader("Number of pickups by hour")
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour,
    bins = 24,
    range=(0, 24))[0]

st.subheader("Map of all pick ups")
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)

fittered_data = data[data[DATE_COLUMN].dt.hour <= hour_to_filter]
st.subheader(f'Map of all pick ups between 00:00 and {hour_to_filter}:00')


st.map(fittered_data)




