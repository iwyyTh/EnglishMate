import streamlit as st
import pandas as pd
import numpy as np
import time
if st.checkbox("Show dataframe"):
    chart_data02 = chart_data

    st.line_chart(chart_data02)


dataframe_03 = pd.DataFrame(
   {
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
   }
)

option = st.selectbox(
    'Which number do you like?',
    dataframe_03['first column']
)

st.write('You selected:', option)

# List thông thường
st.selectbox("Chọn màu", ["Đỏ", "Xanh", "Vàng"])

# Cột DataFrame (như trong code của bạn)
st.selectbox("Chọn số", dataframe_03['first column'])

# Range
st.selectbox("Chọn số", range(1, 10))


add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Mobile phone", "Postal address")
)

add_slider = st.sidebar.slider(
    "Select a range of values",
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)

left_column.button('Click me')

with right_column:
    chosen = st.radio (
        'Sorting hat',
        ('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin')
    )
st.write(f'You are in {chosen}')


'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.01)

'...and now we\'re done!'