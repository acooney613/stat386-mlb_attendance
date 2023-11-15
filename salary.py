import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime

class stadiums():
    def __init__(self, url_1, url_2):
        self.data = pd.DataFrame(columns = ['team', 'location', 'stadium', 'capacity'])
        self.stadium_data(url_1)
        self.stadium_data(url_2)
        self.clean()
        print(self.data)

    def stadium_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        ballparks = soup.find_all('a', class_ = 'stadium-item', href = True)

        for ballpark in ballparks:
            name = ballpark.find('div', class_ = 'title').text
            location = ballpark.find('div', class_ = 'city').text
            tmp_r = requests.get(ballpark['href'])
            tmp_soup = BeautifulSoup(tmp_r.text, 'html.parser')
            info = tmp_soup.find('div', class_ = 'facts-col')
            info = info.find('p').text
            info = info.splitlines()
            team = info[0]
            capacity = info[1]

            row = {'team' : team, 'location' : location, 'stadium' : name, 'capacity' : capacity}
            self.data = pd.concat([self.data, pd.DataFrame(data = row, index = [len(self.data) + 1])], ignore_index = True)
            tmp_r.close()

        r.close()
    
    def clean(self):
        data = self.data
        data[['team']] = data['team'].str.extract(r'\s(\w+\s*\w+)')
        data['location'] = data['location'].str.strip()
        self.data = data
        

        r"\[(.*?)\]"
            


class attendance():
    def __init__(self, base_url):
        self.base_url = base_url
        self.data = pd.DataFrame()
        self.gather()
        
    def collect(self, url, year):
        table = pd.read_html(url)
        df = table[0]
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop = True)
        df = df[[f'{year} Attendance', 'Home']]
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop = True)
        df = df.rename(columns = {'GMS' : f'GMS_{year}', 'RK' : f'RK_{year}', 'TOTAL' : f'TOTAL_{year}',
                         'AVG' : f'AVG_{year}' })
        
        df = df[['TEAM', f'RK_{year}', f'GMS_{year}', f'TOTAL_{year}', f'AVG_{year}']]
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
        self.url_bat = bat
        self.url_pitch = pitch
        self.batter_data()
        self.pitcher_data()
        self.combine()

    def batter_data(self):
        url = self.url_bat
        data = pd.DataFrame(columns = ['team', 'bat_salary'])
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', class_ = 'stats_table')
        tbody = table.find('tbody')
        teams = tbody.find_all('tr')

        for team in teams:
            row = {'team' : team.find('a').text, 'bat_salary' : team.find('td', {'data-stat' : 'Salary'}).text}
            data = pd.concat([data, pd.DataFrame(data = row, index = [len(data) + 1])], ignore_index = True)
        
        data['bat_salary'] = data['bat_salary'].str.replace(',', '')
        data['bat_salary'] = data['bat_salary'].str.extract(r'(\d+)').astype('int')
        self.data_bat = data
        r.close()

    def pitcher_data(self):
        url = self.url_pitch
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

    def combine(self):
        bat = self.data_bat
        pitch = self.data_pitch
        data = pd.merge(bat, pitch, on = 'team', how = 'inner')
        data['salary'] = data['bat_salary'] + data['pitch_salary']

    def dummy():
        pass

#x = salary('https://www.baseball-reference.com/leagues/majors/2023-value-batting.shtml', 
   #        'https://www.baseball-reference.com/leagues/majors/2023-value-pitching.shtml')

#y = attendance('https://www.espn.com/mlb/attendance')

z = stadiums('https://www.ballparksofbaseball.com/american-league/', 'https://www.ballparksofbaseball.com/national-league/')


# could check the change in salary relative to the change in the population size, or the average household income of
# surrounding area
