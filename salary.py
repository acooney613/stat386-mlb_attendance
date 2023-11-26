import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import re

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
        self.pop_stad_att(population)
        # deletes the royals ones why????
        self.sal_pop_stad_att(salary)

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
                        if closed_j >= year_i:
                            row = {'team' : team_j, 'year' : year_i,
                                   'average attendance' : df_attendance.loc[i, 'average attendance'],
                                   'stadium' : df_stadium.loc[j, 'stadium'],
                                   'location' : df_stadium.loc[j, 'location'],
                                   'capacity' : df_stadium.loc[j, 'capacity']}
                            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)

        self.data = data

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
        return self.data

    def combine(self):
        df = pd.merge(self.pop_2010, self.pop_2019, on = 'location')
        df = pd.merge(df, self.pop_2023, on = 'location')
        df = df.melt(id_vars = 'location', 
                     value_vars = ['2003', '2004', '2005', '2006', '2007', '2008', '2009',
                                    '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                                    '2018', '2019', '2020', '2021', '2022'],
                     value_name = 'population',
                     var_name = 'year')
        self.data = df

    def population_2022(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        us = soup.find('li', class_ = 'uscb-list-attachment')
        link = us.find('a', href = True)

        pop_2023 = pd.read_excel('https:' + link['href']).dropna()
        pop_2023.columns = ['location', 'april 2020 base', '2020', '2021', '2022']
        pop_2023['location'] = pop_2023['location'].str.replace(' city', '')
        pop_2023['location'] = pop_2023['location'].str.replace(' City', '')
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
        pop_2019['location'] = pop_2019['location'].str.replace(' City', '')
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
        df[['location']] = df['NAME'].str.extract(r'(.*?)(?:\s*city|\s*City)')
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
                closed = self.data[self.data['location'] == location]['opened'].to_string()
                closed = re.search(r',\s*(.*?)(?:,|\s*\(|$)', closed).group(1)
                closed = int(closed) - 1
                closed = f'{closed}'

                
            else:
                closed = closed.group(1)
                closed = re.search(r',\s*(.*?)(?:,|\s*\(|$)', closed).group(1)
            
            if int(closed) >= 2003:
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
        data['team'] = data['team'].str.replace('Florida', 'Miami')
        data['team'] = data['team'].str.replace('Indians', 'Guardians')
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

class payroll():
    def __init__(self, base_url):
        self.base_url = base_url
        self.pay = pd.DataFrame(columns = ['Team Name', 'Team Payroll', 'year'])
    
    def get_data(self):
        day = datetime.date.today()
        year = day.year - 1
        self.payroll(year)
        self.pay.columns = ['team', 'payroll', 'year']
        self.pay['team'] = self.pay['team'].str.replace(' Devil', '')
        self.pay['team'] = self.pay['team'].str.replace('Los Angeles Angels of Anaheim', 'Los Angeles Angels')
        self.pay['team'] = self.pay['team'].str.replace('Anaheim Angels', 'Los Angeles Angels')
        self.pay['team'] = self.pay['team'].str.replace('Los Angeles Angels of Anaheim', 'Los Angeles Angels')
        self.pay['team'] = self.pay['team'].str.replace('Florida', 'Miami')
        self.pay['team'] = self.pay['team'].str.replace('Montreal Expos', 'Washington Nationals')
        self.pay['team'] = self.pay['team'].str.replace('Oakland Athletics', 'Oakland A’s')
        self.pay['team'] = self.pay['team'].str.replace('Indians', 'Guardians')
        return self.pay

    def payroll(self, year):
        url = self.base_url + f'{year}'
        df = pd.read_html(url)
        pay = df[0]
        pay = pay.iloc[:, [1, 5]]
        pay.columns = pay.loc[0]
        pay = pay.loc[1:30]
        pay['year'] = f'{year}'
        self.pay = pd.concat([self.pay, pay], ignore_index = True)
        if year > 2003:
            self.payroll(year - 1)

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

s = combine(df_payroll, df_stadium, df_pop, df_attendance)
