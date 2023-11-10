import pandas as pd
from bs4 import BeautifulSoup
import requests

class salary():
    def __init__(self, bat, pitch):
        self.url_bat = bat
        self.url_pitch = pitch
        self.batter_data()

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
        print(data)

    def dummy():
        pass

x = salary('https://www.baseball-reference.com/leagues/majors/2023-value-batting.shtml', 
           'https://www.baseball-reference.com/leagues/majors/2023-value-pitching.shtml')





