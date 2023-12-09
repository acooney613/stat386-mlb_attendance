import pandas as pd
import requests
from bs4 import BeautifulSoup

POP2010 = 'Intercensal Estimates of the Resident Population for Incorporated Places and Minor Civil Divisions: April 1, 2000 to July 1, 2010'

class population():
    def __init__(self, url_1, url_2, url_3, url_4, url_5, location):
        self.location = location
        self.url_1 = url_1
        self.url_2 = url_2
        self.url_3 = url_3
        self.url_4 = url_4
        self.url_5 = url_5
        self.canada = pd.DataFrame(columns = ['year', 'population', 'location'])


    def get_data(self):
        self.population_2022(self.url_1)
        self.population_2019(self.url_2)
        self.population_2009(self.url_3)
        self.canadian_data(self.url_4, 'Toronto')
        self.canadian_data(self.url_5, 'Montreal')
        self.combine()
        self.data.to_csv('population.csv', index = False)
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
        
        df = pd.concat([df, self.canada], ignore_index = True)
        df['year'] = df['year'].astype('int')
        df = df[df['year'] > 2002]
        df = df[df['year'] < 2023].reset_index(drop = True)
        self.data = df

    def canadian_data(self, url, city):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table', class_ = 'tp-table-body is-narrow w-full min-w-full table-auto border-separate border-spacing-0 border bg-white')
        items = table.find_all('tr')
        for item in items:
            year = item.find('th')
            pop = item.find('td')
            if pop:
                population = pop.text.strip()
                population = population.replace(',', '')
        
                row = {'year' : year, 'population' : population, 'location' : f'{city}, Canada'}
                self.canada = pd.concat([self.canada,pd.DataFrame(data = row, index = [len(self.canada) + 1])], ignore_index=True)


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

tmp = pd.read_csv('stadiums.csv')
t = population('https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html',
              'https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-cities-and-towns.html',
              'https://www.census.gov/data/datasets/time-series/demo/popest/intercensal-2000-2010-cities-and-towns.html',
              #'https://www.macrotrends.net/cities/20402/toronto/population',
              'https://worldpopulationreview.com/canadian-cities/toronto-population',
              #'https://www.macrotrends.net/cities/20384/montreal/population',
              'https://worldpopulationreview.com/canadian-cities/montreal-population',
              tmp['location'])
df_pop = t.get_data()

print(df_pop)
