import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

# read in the data
df = pd.read_csv('mlb_attendance.csv')

# proportion of fan attendance by payroll with helpful hover data
fig = px.scatter(df, x = 'wins', y = 'proportion', color = 'team', hover_data = ['year'], trendline = 'lowess',
                  trendline_scope='overall', 
                  labels = {
                      'wins' : 'Total Wins',
                      'team' : 'Team',
                      'proportion' : '% Of Total Stadium Capacity',
                      'year' : 'Year'})

fig.update_layout(showlegend = False)
#fig.show()

# scatterplot for payroll and proportion colored by postseason
fig = px.scatter(df, x = 'payroll', y = 'proportion', trendline = 'ols', color = 'made postseason',
                 hover_data = ['year', 'team', "series result"])
#fig.show()

# table to see the average payroll for each postseason category
made_world_average = f'${df[df["postseason"] == 4]["payroll"].mean():,.2f}'
missed_average = f'${df[df["postseason"] == 0]["payroll"].mean():,.2f}'
made_conference_avg = f'${df[df["postseason"] >= 3]["payroll"].mean():,.2f}'
made_division_avg = f'${df[df["postseason"] >= 2]["payroll"].mean():,.2f}'
made_playoffs = f'${df[df["postseason"] >= 1]["payroll"].mean():,.2f}'
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

# scatterplot with lm line for proportion and win-loss
sns.lmplot(data = df, y = 'proportion', x = 'w-l%', palette = 'husl', lowess = False, legend = False, ci = None).set(title = 'Proportion of Stadium Capacity By Record')
plt.xlabel('Win Loss Percentage')
plt.ylabel('Proportion of Stadium Filled (on Average)')
plt.tight_layout()
#plt.savefig('proportion.png')
#plt.show()
plt.close()

# scatterplot with lm line for proportoin and payroll
sns.lmplot(data = df, y = 'proportion', x = 'payroll', hue = 'made postseason', palette = 'husl', lowess = False, legend = False, ci = None).set(title = 'Proportion of Stadium Capacity By Payroll')
plt.tight_layout()
plt.xscale('log')
plt.legend(loc = 'upper left', bbox_to_anchor = (0, 1), title = 'Postseason')
plt.xlabel('Log of Team Payroll')
plt.ylabel('Proportion of Stadium Filled (on Average)')
#plt.savefig('postseason.png')
#plt.show()
plt.close()

# barplot for series result by proportion
df_agg = df.groupby(['series result'])['proportion'].mean().reset_index().sort_values('proportion', ascending = False)
fig = sns.barplot(df, y = 'series result', x = 'proportion', palette = 'husl', errorbar = None, order = df_agg['series result'])
plt.xlabel('Proportion of Stadium Filled')
plt.ylabel('End of Season Result')
plt.title('Effects of Fan Attendance on Season Result')
plt.tight_layout()
#plt.savefig('results.png')
#plt.show()
plt.close()

# barplot of series result by payroll
#order = ['won World Series', 'lost World Series', 'lost ALCS', 'lost NLCS', 'lost ALDS', 'lost NLDS', 'lost ALWC', 'lost NLWC', 'missed postseason']
df_agg = df.groupby(['series result'])['payroll'].mean().reset_index().sort_values('payroll', ascending = False)
fig = sns.barplot(df, y = 'series result', x = 'payroll', palette = 'tab10', errorbar = None, order = df_agg['series result'])
plt.xlabel('Average Team Payroll')
plt.ylabel('End of Season Result')
plt.title('Effects of Payroll on Season Result')
plt.tight_layout()
#plt.show()
#plt.savefig('barchart.png')
plt.close()

# heatmap of correlation values
labels = ['Proportion', 'Population', 'Payroll', 'Record', 'Postseason']
sns.heatmap(df[['proportion', 'population', 'payroll', 'w-l%', 'postseason']].dropna().corr(), 
            xticklabels = labels, cmap = 'rocket_r', yticklabels = labels,
            annot = True)
plt.title('Correlation Matrix')
plt.tight_layout()
#plt.savefig('heatmap.png')
#plt.show()
plt.close()

# bar chart for world series winner and loser stadium proportion
df1 = df[(df['postseason'] == 4 ) & (df['year'] >= 2012)].dropna(subset = ['proportion'])
sns.catplot(data = df1, kind = 'bar', x = 'year', y = 'proportion', hue = 'result', palette = 'husl', legend = False)
plt.xlabel('Year')
plt.ylabel('Proportion of Stadium Filled (On Average)')
plt.title("Season Attendance By Winner and Loser of WS")
plt.legend(loc = 'upper right', title = 'Result')
plt.tight_layout()
#plt.savefig('winner.png')
#plt.show()
plt.close()

# lm plot payroll by win loss 
sns.lmplot(df, x = 'payroll', y = 'w-l%', ci = None, palette = 'husl')
plt.xlabel('Team Payroll')
plt.ylabel('Win-Loss Percentage For Season')
plt.title('Wins by Payroll')
plt.tight_layout()
#plt.savefig('wins_payroll.png')
#plt.show()
plt.close()
