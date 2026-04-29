import streamlit as st
import pandas as pd
import numpy as np
import time

st.write("Here is my first attempt at using data to create a table")
df = pd.DataFrame({
    'col1' : [1, 2, 3, 4],
    'col2' : [10, 20, 30, 40]
})

df

dataframe_01 = np.random.randn(20, 3)
st.dataframe(dataframe_01)

dataframe_02 = pd.DataFrame(
    np.random.randn(10, 20),
    columns=['col %d' % i for i in range(20)]
)
st.dataframe(dataframe_02.style.highlight_max(axis=0))
st.table(dataframe_02.style.highlight_max(axis=0))

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.77, -122.4],
    columns=['lat', 'lon']
)

st.map(map_data)

x = st.slider('x')
st.write(x, 'square is', x * x)





st.text_input("Your name", key='name')

# Hai cách truy cập đều như nhau:
print(st.session_state.name)       # dot notation
print(st.session_state['name'])    # dict notation

# Sử dụng trong logic:
if st.session_state.name:
    st.write(f"Hello, {st.session_state.name}!")




