import pandas as pd

class combine():
    def __init__(self, salary, stadium, population, attendance):
        self.stad_att(stadium, attendance)
        
        #self.pop_stad_att(population)
        #self.sal_pop_stad_att(salary)

    def sal_pop_stad_att(self, salary):
        data = self.data
        data = pd.merge(self.data, salary, on = ['team', 'year'])
        data.to_csv('mlb_attendance.csv')
    
    def pop_stad_att(self, population):
        data = self.data
        data = pd.merge(self.data, population, on = ['location', 'year'])
        self.data = data
    
    def stad_att(self, df_stadium, df_attendance):
        data = pd.DataFrame(columns = ['team', 'year', 'average attendance', 'stadium', 'location', 'capacity'])
        for i in range(len(df_attendance)):
            team_i = df_attendance.loc[i, 'TEAM']
            team_i = team_i.replace('LA ', '')
            team_i = team_i.replace('NY ', '')
            year_i = df_attendance.loc[i, 'year']

            for j in range(len(df_stadium)):
                team_j = df_stadium.loc[j, 'team']
                opened_j = df_stadium.loc[j, 'opened']
                closed_j = df_stadium.loc[j, 'closed']
                
                if team_i in team_j:
                    if closed_j == '-':
                        if opened_j <= year_i:
                            row = {'team' : team_j, 'year' : year_i, 
                                   'average attendance' : df_attendance.loc[i, 'average attendance'],
                                   'stadium' : df_stadium.loc[j, 'stadium'], 
                                   'location' : df_stadium.loc[j, 'location'], 
                                   'capacity' : df_stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
                    
                    else:
                        if int(closed_j) >= year_i:
                            row = {'team' : team_j, 'year' : year_i,
                                   'average attendance' : df_attendance.loc[i, 'average attendance'],
                                   'stadium' : df_stadium.loc[j, 'stadium'],
                                   'location' : df_stadium.loc[j, 'location'],
                                   'capacity' : df_stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
        data.to_csv('test.csv')
        self.data = data
    

df_payroll = pd.read_csv('payroll.csv')
df_stadium = pd.read_csv('stadiums.csv')
df_pop = pd.read_csv('population.csv')
df_attendance = pd.read_csv('attendance.csv')

'''

x = payroll('https://www.thebaseballcube.com/page.asp?PT=payroll_year&ID=')
df_payroll = x.get_data()

y = attendance('https://www.espn.com/mlb/attendance')
df_attendance = y.get_data()

z = stadiums('https://www.ballparksofbaseball.com/american-league/', 'https://www.ballparksofbaseball.com/national-league/', 
            'https://www.ballparksofbaseball.com/past-ballparks/')
df_stadium = z.get_data()

t = population('https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html',
              'https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-cities-and-towns.html',
              'https://www.census.gov/data/datasets/time-series/demo/popest/intercensal-2000-2010-cities-and-towns.html',
              df_stadium['location'])
df_pop = t.get_data()
'''
s = combine(df_payroll, df_stadium, df_pop, df_attendance)
