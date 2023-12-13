import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.title('MLB Attendance Data Exploration')

data = pd.read_csv('mlb_attendance.csv')
data['proportion'] = data['average attendance'] / data['capacity']
data['series_result'] = data['result'] + ' ' + data['series']
data['series_result'] = data['series_result'].fillna('missed postseason')
data['made postseason'] = np.where(data['series'] != 'Missed Postseason', 'Yes', 'No')
numbering = {'World Series' : 4, 'NLCS' : 3, 'ALCS' : 3, 'ALDS' : 2, 'NLDS' : 2, 'NLWC' : 1, 'ALWC' : 1, 'Missed Postseason' : 0}
data['postseason'] = data['series'].map(numbering)

st.subheader('Attendance By Payroll')
st.info('NOTE: The Montreal Expos moved to Washington D.C. in 2005 and became the Washington Nationals')
year = st.number_input('Enter Year', value = None, placeholder = 'enter year between 2003 and 2022', min_value = 2003, 
                       max_value = 2022)

df = data[data['year'] == year]
    
if year == 2020:
    str1 = 'Due to COVID-19 there is no MLB attendance numbers for the year 2020'
    st.markdown(f"<span style = 'color:red'>{str1}</span>", unsafe_allow_html = True)
    
fig1 = px.scatter(df, x = 'payroll', y = 'proportion', color = 'team')

fig1.update_layout(
    xaxis_title='Team Payroll',
    yaxis_title='Proportion of Stadium Capacity Filled',
    title='Attendance by Payroll'
)

st.plotly_chart(fig1)

options = data['team'].unique()
options.sort()

selected = st.multiselect('Select teams:', options = options, default = None)

df2 = data[data['team'].isin(selected)]

fig2 = px.box(df2, y = 'team', x = 'average attendance')
if df2.empty:
    pass
else:
    fig2.update_xaxes(range=[min(df2['average attendance']) - 5000, max(df2['average attendance']) + 5000])


st.plotly_chart(fig2)

