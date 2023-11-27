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
fig = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')

st.plotly_chart(fig)

test = sns.lmplot(data = df, y = 'proportion of capacity filled', x = 'population', lowess = False, legend = False)
#test = plt.xscale('log')

#st.plotly_chart(test)
