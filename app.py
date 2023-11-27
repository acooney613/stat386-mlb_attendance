import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

st.title('MLB Attendance')

data = pd.read_csv('mlb_attendance.csv')
year = st.number_input('Enter Year', value = None, placeholder = 'enter year between 2003 and 2022', min_value = 2003, 
                       max_value = 2022)

data['proportion of capacity filled'] = data['average attendance'] / data['capacity']
df = data[data['year'] == year]
    
if year == 2020:
    str1 = 'Due to COVID-19 there is no MLB attendance numbers for the year 2020'
    st.markdown(f"<span style = 'color:red'>{str1}</span>", unsafe_allow_html = True)
    
fig1 = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')

st.plotly_chart(fig1)

fig2 = px.scatter(data, x = 'population', y = 'average attendance', color = 'year', symbol = 'location')
st.plotly_chart(fig2)



#st.plotly_chart(test)
