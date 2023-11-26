import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

df = pd.read_csv('mlb_attendance.csv')

st.dataframe(df)