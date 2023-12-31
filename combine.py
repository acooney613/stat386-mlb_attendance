import pandas as pd
import numpy as np

class combine():
    def __init__(self, payroll, attendance, stadium, population, season):
        df = self.attendance_stadium(attendance, stadium)
        df = self.combine_population(df, population)
        df = self.combine_payroll(df, payroll)
        self.combine_season(df, season)

    def combine_season(self, data, season):
        data['team'] = data['team'].str.replace('A’s', 'Athletics')
        data = pd.merge(data, season, on = ['team', 'year'])
        data['result'] = data['result'].str.capitalize()
        data['proportion'] = data['average attendance'] / data['capacity']
        data['series result'] = data['result'] + ' ' + data['series']
        data['series result'] = data['series result'].fillna('Missed Postseason')
        data['made postseason'] = np.where(data['series'] != 'Missed Postseason', 'Yes', 'No')
        numbering = {'World Series' : 4, 'NLCS' : 3, 'ALCS' : 3, 'ALDS' : 2, 'NLDS' : 2, 'NLWC' : 1, 'ALWC' : 1, 'Missed Postseason' : 0}
        data['postseason'] = data['series'].map(numbering)
        data = data.rename(columns={'w-l%': 'record'})
        data.to_csv('mlb_attendance.csv', index = False)


    def combine_payroll(self, data, payroll):
        data = pd.merge(data, payroll, on = ['team', 'year'])
        return data

    def combine_population(self, data, population):
        data = pd.merge(data, population, on = ['location', 'year'])
        return data

    def attendance_stadium(self, attendance, stadium):
        data = pd.DataFrame(columns = ['team', 'year', 'average attendance', 'stadium', 'location', 'capacity'])
        for i in range(len(attendance)):
            team_i = attendance.loc[i, 'TEAM']
            team_i = team_i.replace('LA ', '')
            team_i = team_i.replace('NY ', '')
            year = attendance.loc[i, 'year']

            for j in range(len(stadium)):
                team_j = stadium.loc[j, 'team']
                opened = stadium.loc[j, 'opened']
                closed = stadium.loc[j, 'closed']
            
                if team_i in team_j:
                    if closed == '-':
                        if opened <= year:
                            row = {'team' : team_j, 'year' : year, 
                                   'average attendance' : attendance.loc[i, 'average attendance'],
                                   'stadium' : stadium.loc[j, 'stadium'], 
                                   'location' : stadium.loc[j, 'location'], 
                                   'capacity' : stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
                        
                    else:
                        if int(closed) >= year:
                            row = {'team' : team_j, 'year' : year,
                                   'average attendance' : df_attendance.loc[i, 'average attendance'],
                                   'stadium' : df_stadium.loc[j, 'stadium'],
                                   'location' : df_stadium.loc[j, 'location'],
                                   'capacity' : df_stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
        return data

# must create these CSV's using the respective files
df_payroll = pd.read_csv('DATA/payroll.csv')
df_stadium = pd.read_csv('DATA/stadiums.csv')
df_pop = pd.read_csv('DATA/population.csv')
df_attendance = pd.read_csv('DATA/attendance.csv')
season = pd.read_csv('DATA/season.csv')

comb = combine(df_payroll, df_attendance, df_stadium, df_pop, season)