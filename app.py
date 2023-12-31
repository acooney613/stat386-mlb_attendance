import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

data = pd.read_csv('mlb_attendance.csv')
order = ['Missed Postseason', 'Lost NLWC', 'Lost ALWC', 'Lost NLDS', 'Lost ALDS', 'Lost NLCS', 'Lost ALCS', 'Lost World Series', 'Won World Series']
#order = ['Won World Series', 'Lost World Series', 'Lost ALCS', 'Lost NLCS', 'Lost ALDS', 'Lost NLDS', 'Lost ALWC', 'Lost NLWC', 'Missed Postseason']
data['series result'] = pd.Categorical(data['series result'], categories=order, ordered=True)

st.set_page_config(layout="wide")
title = """
    <div style="display: flex; justify-content: center; align-items: center;">
        <h1>MLB Attendance Data</h1>
    </div>
"""

st.markdown(title, unsafe_allow_html=True)

cols = st.columns([1, 3, 1])

text = 'This app is designed to help you explore data that contains information about MLB teams from 2003 to 2022.'
text2 = '\n\nIt is important to note that for the year 2020, the MLB did not have any attendance data due to COVID-19.'
text3 = '\n\nIf you would like to learn more about this data and how it was collected I would encourage you to loop through my'
text4 = ' [repo](https://github.com/acooney613/stat386-mlb_attendance) as well as explore my [data collection blog](https://acooney613.github.io/2023/12/10/post-dataclean.html)'
text5 = ' and [data visualization blog](https://acooney613.github.io/2023/12/12/post-dataviz.html).'
text6 = '\n\nHave fun exploring the data below!!'

cols[1].markdown(text+text2+text3+text4+text5+text6, unsafe_allow_html=True)

avg = data.groupby('made postseason').mean('average attendance')[['average attendance']].reset_index()
avg['year'] = 'Overall'

st.subheader('Data By Year')
st.info('NOTE: The Montreal Expos moved to Washington D.C. in 2005 and became the Washington Nationals')

year = st.number_input('Enter Year', value = None, placeholder = 'enter year between 2003 and 2022', min_value = 2003, 
                       max_value = 2022)


df = data[data['year'] == year]
    
if year == 2020:
    str1 = 'Due to COVID-19 there is no MLB attendance numbers for the year 2020'
    st.markdown(f"<span style = 'color:red'>{str1}</span>", unsafe_allow_html = True)
    
fig1 = px.scatter(df, x = 'payroll', y = 'proportion', color = 'team', hover_data = ['series result', 'wins'],
                  labels = {
                      'wins' : 'Total Wins',
                      'series result' : 'Season Result',
                      'payroll' : 'Team Payroll',
                      'proportion' : 'Stadium Proportion',
                      'team' : 'Team',
                  })
 
df['avg'] = df['made postseason']
curr_avg = df.groupby('made postseason').mean('average attendance')[['average attendance']].reset_index()
curr_avg['year'] = f'Current ({year})'
tmp = pd.concat([curr_avg, avg], ignore_index=True)
test = px.bar(tmp, x = 'made postseason', y = 'average attendance', color = 'year',
              labels = {
                  'made postseason' : 'Made Postseason',
                  'average attendance' : 'Average Attendance',
                  'year' : 'Year'
              })
test.update_layout(title=f'{year} vs Overall Attendance', barmode='group', xaxis_title='Made The Postseason (Yes or No)', yaxis_title='Average Attendance', title_x = 0.2)

fig1.update_traces(showlegend = False)

fig1.update_layout(
    xaxis_title='Team Payroll',
    yaxis_title='Proportion of Stadium Capacity Filled',
    title='Attendance by Payroll',
    title_x = 0.4
)

cols = st.columns([2, 1])
fig1.update_layout(width=800, height=500)
test.update_layout(width = 450, height = 500)
cols[0].plotly_chart(fig1, config = {'displayModeBar' : False})
cols[0].info("This shows the percent of the stadium filled (on average) by total payroll, colored by team \n\nNOTE: Hovering over each point will show more information about that team's season")
cols[1].plotly_chart(test, config = {'displayModeBar' : False})
cols[1].info(f"This is a bar chart comparing the overall average attendance and the current year's average attendance")

options = data['team'].unique()
options.sort()

st.subheader('Data By Team')
st.info('NOTE: Due to the shortened 2020 season the scatterplot does not contain information for that season')

selected = st.multiselect('Select teams:', options = options, default = None)
cols = st.columns(2)
df2 = data[data['team'].isin(selected)]

fig2 = px.box(df2, y = 'team', x = 'average attendance',
              labels = {
                  'team' : 'Team',
                  'average attendance' : 'Average Attendance'
              })
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

cols[0].plotly_chart(fig2)
cols[0].info("Boxplot for the selected team's average attendance")

if not selected:
    fig3 = px.scatter(df2, x = 'wins', y = 'proportion', color = 'team', 
                      labels = {
                      'wins' : 'Total Wins',
                      'team' : 'Team',
                      'proportion' : '% Of Total Stadium Capacity'})

else:
    fig3 = px.scatter(df2, x = 'wins', y = 'proportion', color = 'team', color_continuous_scale='Viridis', hover_data = ['year', 'series result'], trendline = 'lowess', 
                  labels = {
                      'wins' : 'Total Wins',
                      'team' : 'Team',
                      'proportion' : 'Stadium Proportion',
                      'year' : 'Year',
                      'series_result' : 'Season Result'})
    fig3.update_layout(showlegend = False)
    df2 = df2[df2['year'] != 2020]
    X_max = df2['wins'].max()
    X_min = df2['wins'].min()
    fig3.update_xaxes(range = [X_min - 5, X_max + 5])

fig3.update_layout(
    xaxis_title='Total Wins',
    yaxis_title='Proportion of Stadium Capacity Filled',
    title='Attendance By Wins',
    title_x = 0.4
)

cols[1].plotly_chart(fig3)
cols[1].info("This shows the percent of the stadium filled (on average) by total wins, colored by team")

st.subheader('Filter Dataset')
col1, col2, col3 = st.columns(3)
data['average attendance'].fillna(value = 'COVID-19', inplace = True)
data['proportion'].fillna(value = 'COVID-19', inplace = True)
with col1:
    years = data['year'].unique()
    year = st.selectbox('Select Year To Look At: ', options = years, index = None)
    df3 = data[data['year'] == year]
    df3.drop(columns = 'year')

with col2:
    options = list(data.columns)
    options.remove('year')
    options.remove('team')
    options.remove('result')
    options.remove('series')
    options.sort()
    selected = st.multiselect('Select columns:', options = options, default = None)
    select = ['team'] + selected
    df3 = df3[select]

with col3:
    column = st.selectbox('Column To Sort By: ', list(df3.columns), index = None)

value = not st.checkbox('Sort Highest To Lowest', value = True)
if column:
    df3 = df3.sort_values(by = column, ascending = value)


#df3 = df3.fillna('COVID-19')
df3 = df3.reset_index(drop = True)

st.table(df3)