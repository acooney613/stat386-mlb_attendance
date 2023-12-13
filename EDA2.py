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
made_playoffs = f'${df[df["code"] >= 1]["payroll"].mean():,.2f}'
data = [['Season Result', 'Average Payroll (2003 - 2022)'],
        ['Made World Series', made_world_average],
        ['Made NLCS or ALCS', made_conference_avg],
        ['Made ALDS or NLDS', made_division_avg],
        ['Made Playoffs', made_playoffs],
        ['Missed Playoffs', missed_average]]
fig, ax = plt.subplots()
table = plt.table(cellText = data, cellLoc='center', loc='center')
ax.axis('off')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)
#plt.show()
plt.close()
ax.axis('on')

# Question 4: Do teams that go farther into the playoffs tend to spend more?
fig = sns.barplot(df, y = 'series_result', x = 'payroll', errorbar = None)
plt.tight_layout()
plt.xlabel('Average Team Payroll')
plt.ylabel('End of Season Result')
#plt.savefig('barchart.png')
#plt.show()
plt.close()

# Question 5: Affects of Payroll on Attendance
sns.lmplot(data = df, y = 'proportion', x = 'wins', lowess = False, legend = False, ci = None).set(title = 'Proportion of Stadium Capacity By Population')
plt.tight_layout()
#plt.savefig('proportion.png')
#plt.show()
plt.close()

sns.lmplot(data = df, y = 'proportion', x = 'payroll', hue = 'postseason', palette = 'husl', lowess = False, legend = False, ci = None).set(title = 'Proportion of Stadium Capacity By Population')
plt.tight_layout()
plt.xscale('log')
plt.legend(loc = 'upper left', bbox_to_anchor = (0, 1), title = 'Postseason')
plt.xlabel('Log of Team Payroll')
plt.ylabel('Proportion of Stadium Filled (on Average)')
plt.savefig('postseason.png')
plt.show()


