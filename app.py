import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

st.title('MLB Attendance')

data = pd.read_csv('mlb_attendance.csv')
year = st.number_input('Enter Year', value = None, placeholder = 'enter year between 2003 and 2022', min_value = 2003, max_value = 2022)

data['proportion of capacity filled'] = data['average attendance'] / data['capacity']

df = data[data['year'] == year]
fig1 = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team', trendline = 'ols', trendline_scope = 'overall')

st.plotly_chart(fig1)

fig2 = px.scatter(df, x = 'population', y = 'payroll', trendline = 'ols')
st.plotly_chart(fig2)



#st.plotly_chart(test)
