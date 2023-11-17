import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re
import numpy as np

POP2010 = 'Intercensal Estimates of the Resident Population for Incorporated Places and Minor Civil Divisions: April 1, 2000 to July 1, 2010'

STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

class combine():
    def __init__(self, salary, stadium, population, attendance):
        self.stad_att(stadium, attendance)
    
    def stad_att(sel, df_stadium, df_attendance):
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
                        if closed_j > year_i:
                            row = {'team' : team_j, 'year' : year_i,
                                   'average attendance' : df_attendance.loc[i, 'average attendance'],
                                   'stadium' : df_stadium.loc[j, 'stadium'],
                                   'location' : df_stadium.loc[j, 'location'],
                                   'capacity' : df_stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)

        print(data)

class population():
    def __init__(self, url_1, url_2, url_3, location):
        self.location = location
        self.url_1 = url_1
        self.url_2 = url_2
        self.url_3 = url_3

    def get_data(self):
        self.population_2022(self.url_1)
        self.population_2019(self.url_2)
        self.population_2009(self.url_3)
        self.combine()

    def combine(self):
        df = pd.merge(self.pop_2010, self.pop_2019, on = 'location')
        df = pd.merge(df, self.pop_2023, on = 'location')
        print(df.columns)
        df = df.melt(id_vars = 'location', 
                     value_vars = ['2003', '2004', '2005', '2006', '2007', '2008', '2009',
                                    '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                                    '2018', '2019', '2020', '2021', '2022'],
                     value_name = 'population',
                     var_name = 'year')
        print(df)

    def population_2022(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        us = soup.find('li', class_ = 'uscb-list-attachment')
        link = us.find('a', href = True)

        pop_2023 = pd.read_excel('https:' + link['href']).dropna()
        pop_2023.columns = ['location', 'april 2020 base', '2020', '2021', '2022']
        pop_2023['location'] = pop_2023['location'].str.replace(' city', '')
        pop_2023['2021'] = pop_2023['2021'].astype('int')
        pop_2023['2022'] = pop_2023['2022'].astype('int')
        mask = pop_2023['location'].isin(self.location)
        pop_2023 = pop_2023[mask]
        pop_2023 = pop_2023[['location', '2020', '2021', '2022']].reset_index(drop = True)
        self.pop_2023 = pop_2023

    def population_2019(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        us = soup.find('li', class_ = 'uscb-list-attachment')
        link = us.find('a', href = True)

        pop_2019 = pd.read_excel('https:' + link['href']).dropna().reset_index(drop = True)
        pop_2019.columns = ['location', 'census', 'estimate base', '2010', '2011', '2012', '2013', '2014', '2015',
                             '2016', '2017', '2018', '2019']
        
        pop_2019['location'] = pop_2019['location'].str.replace(' city', '')
        pop_2019['2011'] = pop_2019['2011'].astype('int')
        pop_2019['2012'] = pop_2019['2012'].astype('int')
        pop_2019['2013'] = pop_2019['2013'].astype('int')
        pop_2019['2014'] = pop_2019['2014'].astype('int')
        pop_2019['2015'] = pop_2019['2015'].astype('int')
        pop_2019['2016'] = pop_2019['2016'].astype('int')
        pop_2019['2017'] = pop_2019['2017'].astype('int')
        pop_2019['2018'] = pop_2019['2018'].astype('int')
        pop_2019['2019'] = pop_2019['2019'].astype('int')

        mask = pop_2019['location'].isin(self.location)
        pop_2019 = pop_2019[mask]

        pop_2019 = pop_2019[['location', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                             '2017', '2018', '2019']].reset_index(drop = True)
        
        self.pop_2019 = pop_2019
    
    def population_2009(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        us = soup.find('a', {'name' : POP2010}, href = True)
        new_url = 'https:' + us['href']
        df = pd.read_csv(new_url, encoding = 'ISO-8859-1')
        df = df[['NAME', 'STNAME', 'POPESTIMATE2003', 'POPESTIMATE2004', 'POPESTIMATE2005',
                            'POPESTIMATE2006', 'POPESTIMATE2007', 'POPESTIMATE2008', 'POPESTIMATE2009',
                            'POPESTIMATE2010']]
        df.columns = ['NAME', 'STNAME', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
        df[['location']] = df['NAME'].str.extract(r'(.*?)(?:\s*city)')
        df = df.dropna()
        df['location'] = df['location'] + ', ' + df['STNAME']
        mask = df['location'].isin(self.location)
        df = df[mask]
        df = df[['location', '2003', '2004', '2005', '2006', '2007', '2008', '2009']]
        
        df = df.drop_duplicates('location', keep = 'first').reset_index(drop = True)
        self.pop_2010 = df

class stadiums():
    def __init__(self, url_1, url_2, url_3):
        self.data = pd.DataFrame(columns = ['team', 'location', 'stadium', 'capacity', 'opened', 'closed'])
        self.url_1 = url_1
        self.url_2 = url_2
        self.url_3 = url_3
    
    def get_data(self):
        self.stadium_data(self.url_1)
        self.stadium_data(self.url_2)
        self.past_stadium(self.url_3)
        self.clean()
        return self.data

    def past_stadium(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        ballparks = soup.find_all('a', class_ = 'stadium-item', href = True)

        for ballpark in ballparks:
            name = ballpark.find('div', class_ = 'title').text
            location = ballpark.find('div', class_ = 'city').text.strip()
            tmp_r = requests.get(ballpark['href'])
            tmp_soup = BeautifulSoup(tmp_r.text, 'html.parser')
            info = tmp_soup.find_all('div', class_ = 'facts-col')
            tmp = ''
            for x in info:
                tmp = tmp + x.find('p').text + '\n'
            
            team = re.search(r'(?:Tenant|Tenants):\s*(.*?)\n', tmp).group(1)
            capacity = re.search(r'Capacity:\s*(.*?)\n', tmp).group(1)
            opened = re.search(r'(?:Opened|Opening):\s*(.*?)\n', tmp).group(1)
            closed = re.search(r'Closed:\s*(.*?)\n', tmp)
            if closed == None:
                closed = '-'
                closed = self.data[self.data['location'] == location]['opened'].to_string()
                
            else:
                closed = closed.group(1)

            closed = re.search(r',\s*(.*?)(?:,|\s*\(|$)', closed).group(1)
            
            if int(closed) > 2003:
                row = {'team' : team, 'location' : location, 'stadium' : name, 'capacity' : capacity, 'opened' : opened, 'closed' : closed}
                self.data = pd.concat([self.data, pd.DataFrame(data = row, index = [len(self.data) + 1])], ignore_index = True)
            tmp_r.close()
        r.close()

        
    def stadium_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        ballparks = soup.find_all('a', class_ = 'stadium-item', href = True)

        for ballpark in ballparks:
            name = ballpark.find('div', class_ = 'title').text
            location = ballpark.find('div', class_ = 'city').text.strip()
            tmp_r = requests.get(ballpark['href'])
            tmp_soup = BeautifulSoup(tmp_r.text, 'html.parser')
            info = tmp_soup.find('div', class_ = 'facts-col')
            info = info.find('p').text
            team = re.search(r'-(?:Tenant|Tenants):\s*(.*?)\n', info).group(1)
            capacity = re.search(r'-Capacity:\s*(.*?)\n', info).group(1)
            opened = re.search(r'-(?:Opened|Opening):\s*(.*?)\n', info).group(1)

            row = {'team' : team, 'location' : location, 'stadium' : name, 'capacity' : capacity, 'opened' : opened, 'closed' : '-'}
            self.data = pd.concat([self.data, pd.DataFrame(data = row, index = [len(self.data) + 1])], ignore_index = True)
            tmp_r.close()
        r.close()
    
    def clean(self):
        data = self.data
        data[['team']] = data['team'].str.extract(r'\s*(.*?)(?:,|\(|$)')
        data['team'] = data['team'].str.strip()
        data['location'] = data['location'].str.strip()
        data['capacity'] = data['capacity'].str.replace(',', '')
        data['capacity'] = data['capacity'].str.extract(r'(\d+)').astype('int')
        data[['city']] = data['location'].str.extract(r'(.*?)(?:,)')
        data['city'] = data['city'].replace(['Bronx', 'Queens', 'Flushing'], 'New York City')
        data[['state']] = data['location'].str.extract(r',\s*(\w+)')
        data[['opened']] = data['opened'].str.extract(r',\s*(.*?)(?:,|\s*\(|$)')
        data[['city']] = data['city'].str.extract(r'(.*?)(?:\s*City|$)')
        data['state'] = data['state'].map(STATES)
        data['location'] = data['city'] + ', ' + data['state']
        self.data = data[['team', 'location', 'stadium', 'capacity', 'opened', 'closed']].dropna().reset_index(drop = True)

        # need to merge on both the team and the year, to get the right stadium and location
        # need to add a year column to the attendance dataset or something


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
        df['TEAM'] = df['TEAM'].str.replace('Montreal', 'Washington')

        if self.data.empty:
            self.data = df
        else:
            self.data = pd.merge(self.data, df, on = 'TEAM', how = 'inner').rename_axis(None).reset_index(drop = True)

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



class salary():
    def __init__(self, bat, pitch):
        # this website has a too many requests error
        self.url_bat = bat
        self.url_pitch = pitch
    
    def get_data(self):
        self.data = pd.DataFrame(columns = ['team', 'bat_salary', 'year'])
        self.batter_data(self.url_bat)
        self.clean()
        #self.pitcher_data(self.url_pitch)
        #self.combine()
        # only want the overall salary
        # need to get for different years !!!!
        return self.data


    def batter_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
    
        year = soup.find('h1').text
        year = re.search(r'(\d+)', year).group(1)

        table = soup.find('table', class_ = 'stats_table')
        tbody = table.find('tbody')
        teams = tbody.find_all('tr')

        for team in teams:
            row = {'team' : team.find('a').text, 'bat_salary' : team.find('td', {'data-stat' : 'Salary'}).text, 'year' : year}
            self.data = pd.concat([self.data, pd.DataFrame(data = row, index = [len(self.data) + 1])], ignore_index = True)

        #self.data['bat_salary'] = self.data['bat_salary'].str.replace(',', '')
        #self.data['bat_salary'] = self.data['bat_salary'].str.extract(r'(\d+)').astype('int')
    
        if int(year) > 2003:
            base_url = 'https://www.baseball-reference.com'
            prev_url = soup.find('a', href = True, class_ = 'button2 prev')
            self.batter_data(base_url + prev_url['href'])

        r.close()

    def pitcher_data(self, url):
        
        data = pd.DataFrame(columns = ['team', 'pitch_salary'])
        r = requests.get(url)
        soup = BeautifulSoup(r.text ,'html.parser')

        table = soup.find('table', class_ = 'stats_table')
        tbody = table.find('tbody')
        teams = tbody.find_all('tr')

        for team in teams:
            row = {'team' : team.find('a').text, 'pitch_salary' : team.find('td', {'data-stat' : 'Salary'}).text}
            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
        
        data['pitch_salary'] = data['pitch_salary'].str.replace(',', '')
        data['pitch_salary'] = data['pitch_salary'].str.extract(r'(\d+)').astype('int')
        self.data_pitch = data
        r.close()
    
    def clean(self):
        self.data['bat_salary'] = self.data['bat_salary'].str.replace(',', '')
        self.data['bat_salary'] = self.data['bat_salary'].str.extract(r'(\d+)').astype('int')

    def combine(self):
        bat = self.data_bat
        pitch = self.data_pitch
        data = pd.merge(bat, pitch, on = 'team', how = 'inner')
        data['salary'] = data['bat_salary'] + data['pitch_salary']
        self.data = data

#x = salary('https://www.baseball-reference.com/leagues/majors/2023-value-batting.shtml', 
#         'https://www.baseball-reference.com/leagues/majors/2023-value-pitching.shtml')

#df_salary = x.get_data()
#print(df_salary)

y = attendance('https://www.espn.com/mlb/attendance')

df_attendance = y.get_data()
#print(df_attendance)

z = stadiums('https://www.ballparksofbaseball.com/american-league/', 'https://www.ballparksofbaseball.com/national-league/', 
            'https://www.ballparksofbaseball.com/past-ballparks/')

df_stadium = z.get_data()

s = combine(None, df_stadium, None, df_attendance)


'''
t = population('https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html',
              'https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-cities-and-towns.html',
              'https://www.census.gov/data/datasets/time-series/demo/popest/intercensal-2000-2010-cities-and-towns.html',
              location)
df_pop = t.get_data()
'''

# when going to combine, we can first combine the stadium and slary data on team and year
# in which case we should replicate the years for the stadiums
# then we can merge the population data with the new locations and years as well for the complete and final dataset
# attendance will be added also by team and year 