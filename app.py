import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.title('MLB Attendance')

df = pd.read_csv('mlb_attendance.csv')
print(df)

df['proportion of capacity filled'] = df['average attendance'] / df['capacity']
fig = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')

st.plotly_chart(fig)