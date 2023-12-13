import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.title('MLB Attendance Data Exploration')
text = 'This app uses data that was collected and scraped from several different webpages using code found in [this repo](https://github.com/acooney613/stat386-mlb_attendance).' +' It is also important to note that due to COVID-19 there are no MLB attendance numbers for the year 2020.' + ' Have fun exploring this dataset and feel free to take a look at my repo and [blog](https://acooney613.github.io/) to see how the data was collected and used.'
st.markdown(text, unsafe_allow_html=True)
data = pd.read_csv('mlb_attendance.csv')
numbering = {'World Series' : 4, 'NLCS' : 3, 'ALCS' : 3, 'ALDS' : 2, 'NLDS' : 2, 'NLWC' : 1, 'ALWC' : 1, 'Missed Postseason' : 0}
data['postseason'] = data['series'].map(numbering)
data['proportion'] = data['average attendance'] / data['capacity']
data['series_result'] = data['result'] + ' ' + data['series']
data['series_result'] = data['series_result'].fillna('missed postseason')
data['made postseason'] = np.where(data['series'] != 'Missed Postseason', 'Yes', 'No')

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
    title='Attendance by Payroll',
    title_x = 0.3
)

st.plotly_chart(fig1)

options = data['team'].unique()
options.sort()

st.subheader('Boxplots Of Team Average Attendance')
selected = st.multiselect('Select teams:', options = options, default = None)

df2 = data[data['team'].isin(selected)]

fig2 = px.box(df2, y = 'team', x = 'average attendance')
if df2.empty:
    pass
else:
    fig2.update_xaxes(range=[min(df2['average attendance']) - 5000, max(df2['average attendance']) + 5000])

fig2.update_layout(
    xaxis_title='Attendance',
    yaxis_title='Teams Selected',
    title='Attendence Plots For Teams Selected',
    title_x = 0.3
)

st.plotly_chart(fig2)
fig3 = sns.catplot(df, kind = 'bar', x = 'year', y = 'proportion', hue = 'team', palettee = 'husl', legend = False)

st.plotly_chart(fig3)
