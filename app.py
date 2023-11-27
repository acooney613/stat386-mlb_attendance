import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.title('MLB Attendance')

data = pd.read_csv('mlb_attendance.csv')
year = st.text_input('Enter Year', '2022')

data['proportion of capacity filled'] = data['average attendance'] / data['capacity']

df = data[data['year'] == int(year)]
print(df)
fig = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')

st.plotly_chart(fig)