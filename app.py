import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

col = st.columns(3)

col[1].title('MLB Attendance Data')
text = 'This app is designed to help you explore data that contains information about MLB teams from 2003 to 2022.'
text2 = '\n\nIt is important to note that for the year 2020, the MLB did not have any attendance data due to COVID-19.'
text3 = '\n\nIf you would like to learn more about this data and how it was collected I would encourage you to loop through my'
text4 = '[repo](https://github.com/acooney613/stat386-mlb_attendance) as well as explore my [data collection blog](https://acooney613.github.io/2023/12/10/post-dataclean.html)'
text5 = ' and [data visualization blog](https://acooney613.github.io/2023/12/12/post-dataviz.html).'
text6 = '\n\nHave fun exploring the data below!!'

st.markdown(text+text2+text3+text4+text5+text6, unsafe_allow_html=True)

data = pd.read_csv('mlb_attendance.csv')
numbering = {'World Series' : 4, 'NLCS' : 3, 'ALCS' : 3, 'ALDS' : 2, 'NLDS' : 2, 'NLWC' : 1, 'ALWC' : 1, 'Missed Postseason' : 0}
data['postseason'] = data['series'].map(numbering)
data['proportion'] = data['average attendance'] / data['capacity']
data['series_result'] = data['result'] + ' ' + data['series']
data['series_result'] = data['series_result'].fillna('missed postseason')
data['made postseason'] = np.where(data['series'] != 'Missed Postseason', 'Yes', 'No')

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
    
fig1 = px.scatter(df, x = 'payroll', y = 'proportion', color = 'team', hover_data = ['series_result', 'wins'],
                  labels = {
                      'wins' : 'Total Wins',
                      'series_result' : 'Season Result',
                      'payroll' : 'Team Payroll',
                      'proportion' : 'Stadium Proportion'
                  })
 
df['avg'] = df['made postseason']
curr_avg = df.groupby('made postseason').mean('average attendance')[['average attendance']].reset_index()
curr_avg['year'] = f'Current ({year})'
tmp = pd.concat([curr_avg, avg], ignore_index=True)
test = px.bar(tmp, x = 'made postseason', y = 'average attendance', color = 'year')
test.update_layout(title=f'{year} vs Overall', barmode='group', xaxis_title='Made The Postseason (Yes or No)', yaxis_title='Average Attendance', title_x = 0.3)

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
cols[1].plotly_chart(test, config = {'displayModeBar' : False})

options = data['team'].unique()
options.sort()

st.subheader('Data By Team')
st.info('NOTE: Due to the shortened 2020 season the scatterplot does not contain information for that season')

selected = st.multiselect('Select teams:', options = options, default = None)
cols = st.columns(2)
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

cols[0].plotly_chart(fig2)

if not selected:
    fig3 = px.scatter(df2, x = 'wins', y = 'proportion', color = 'team', 
                      labels = {
                      'wins' : 'Total Wins',
                      'team' : 'Team',
                      'proportion' : '% Of Total Stadium Capacity'})

else:
    fig3 = px.scatter(df2, x = 'wins', y = 'proportion', color = 'team', color_continuous_scale='Viridis', hover_data = ['year', 'series_result'], trendline = 'lowess', 
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

st.subheader('Filter Dataset')
col1, col2, col3 = st.columns(3)

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
    column = st.selectbox('Column To Sort By: ', list(df3.columns), index = 0)

value = not st.checkbox('Sort Highest To Lowest', value = True)
df3 = df3.sort_values(by = column, ascending = value)

df3 = df3.fillna('COVID-19')
df3 = df3.reset_index(drop = True)

st.table(df3)