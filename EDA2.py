import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

# read in the data
df = pd.read_csv('mlb_attendance.csv')
df['proportion'] = df['average attendance'] / df['capacity']
df['series_result'] = df['result'] + ' ' + df['series']
df['series_result'] = df['series_result'].fillna('missed postseason')
df['postseason'] = np.where(df['series'] != 'Missed Postseason', 'Yes', 'No')

numbering = {'World Series' : 4, 'NLCS' : 3, 'ALCS' : 3, 'ALDS' : 2, 'NLDS' : 2, 'NLWC' : 1, 'ALWC' : 1, 'Missed Postseason' : 0}
df['code'] = df['series'].map(numbering)
# Question 1: Does more wins lead to greater fan attendance?
fig = px.scatter(df, x = 'wins', y = 'proportion', color = 'team', hover_data = ['year'], trendline = 'lowess',
                  trendline_scope='overall', 
                  labels = {
                      'wins' : 'Total Wins',
                      'team' : 'Team',
                      'proportion' : '% Of Total Stadium Capacity',
                      'year' : 'Year'})

fig.update_layout(showlegend = False)
#fig.show()

# Question 2: Does spending more lead to more success and fans?
fig = px.scatter(df, x = 'payroll', y = 'proportion', trendline = 'ols', color = 'postseason',
                 hover_data = ['year', 'team', 'series_result'])
#fig.show()

# Question 3: Do postseason teams have a higher payroll?
made_world_average = f'${df[df["code"] == 4]["payroll"].mean():,.2f}'
missed_average = f'${df[df["code"] == 0]["payroll"].mean():,.2f}'
made_conference_avg = f'${df[df["code"] >= 3]["payroll"].mean():,.2f}'
made_division_avg = f'${df[df["code"] >= 2]["payroll"].mean():,.2f}'
data = [['Season Result', 'Average Payroll (2003 - 2022)']]
plt.table(cellText = )



