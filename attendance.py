import pandas as pd
import datetime

class attendance():
    def __init__(self, base_url):
        self.base_url = base_url
        self.data = pd.DataFrame()

    def get_data(self):
        self.gather()
        self.data = self.data.melt(id_vars = 'TEAM', 
                                   value_vars = ['2023', '2022', '2021', '2019', '2018', '2017',
                                                 '2016', '2015', '2014', '2013', '2012',
                                                  '2011', '2010', '2009', '2008', '2007', '2006',
                                                   '2005', '2004', '2003' ],
                                    value_name = 'average attendance',
                                    var_name = 'year')
        
        self.data.to_csv('attendance.csv')
        return self.data


    def collect(self, url, year):
        table = pd.read_html(url)
        df = table[0]
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop = True)
        df = df[[f'{year} Attendance', 'Home']]
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop = True)
        df = df.rename(columns = {'AVG' : f'{year}' })
        
        df = df[['TEAM', f'{year}']]
        df['TEAM'] = df['TEAM'].str.replace('Florida', 'Miami')
        df['TEAM'] = df['TEAM'].str.replace('Anaheim', 'LA Angels')
        #df['TEAM'] = df['TEAM'].str.replace('Montreal', 'Washington')
        print(df)
        if self.data.empty:
            self.data = df
        else:
            self.data = pd.merge(self.data, df, on = 'TEAM', how = 'outer').rename_axis(None).reset_index(drop = True)

    def gather(self):
        dt = datetime.date.today()
        year = dt.year
        while year > 2002:
            if year == 2020:
                year -= 1
            if year == dt.year:
                self.collect(self.base_url, year)
                year -= 1
            else:
                extend = f'/_/year/{year}'
                self.collect(self.base_url + extend, year)
                year -= 1

y = attendance('https://www.espn.com/mlb/attendance')
df_attendance = y.get_data()