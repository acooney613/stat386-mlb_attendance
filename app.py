import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

df = pd.read_csv('mlb_attendance.csv')

df['proportion of capacity filled'] = df['average attendance'] / df['capacity']
fig = px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')

st.title('Proportion of Stadium Capacity Filled')
st.plotly_chart(fig)