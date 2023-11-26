import streamlit as st
import pandas as pd

df = pd.read_csv('mlb_attendance.csv')

st.dataframe(df)