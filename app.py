import streamlit as st
import pandas as pd
#import seaborn as sns

df = pd.read_csv('mlb_attendance.csv')

st.dataframe(df)