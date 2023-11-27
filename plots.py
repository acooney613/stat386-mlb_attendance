#%%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

#%%
df = pd.read_csv('mlb_attendance.csv')

# %%
sns.boxplot(data = df, y = 'team', x = 'average attendance').set(title = 'boxplot for average attendance')
plt.xlabel('average attendance (2003 - 2022)')

# %%
sns.lmplot(data = df, x = 'payroll', y = 'average attendance', lowess = True, legend = False)
plt.xscale('log')
# %%
sns.pairplot(data = df, palette = 'Set2')

# %%
df['proportion of capacity filled'] = df['average attendance'] / df['capacity']
px.scatter(df, x = 'payroll', y = 'proportion of capacity filled', color = 'team')
# %%
sns.lmplot(data = df, y = 'proportion of capacity filled', x = 'population', lowess = False, legend = False).set(title = 'portion of stadium capacity by population')
plt.xscale('log')
# %%
sns.lmplot(data = df, y = 'proportion of capacity filled', x = 'payroll', lowess = False, legend = False, ci = None).set(title = 'portion of stadium capacity by population')
plt.xscale('log')
# %%
