import pandas as pd
import datetime

class seasons():
    def __init__(self):
        self.get_standings()
        self.get_results()
        self.merge()

    def merge(self):
        
        season = pd.merge(self.standings, self.result, how = 'outer', on = ['team', 'year'])
        season['series'] = season['series'].fillna('Missed Postseason')

        season['team'] = season['team'].str.replace('Los Angeles Angels of Anaheim', 'Los Angeles Angels')
        season['team'] = season['team'].str.replace('Anaheim Angels', 'Los Angeles Angels')
        season['team'] = season['team'].str.replace('Indians', 'Guardians')
        season['team'] = season['team'].str.replace(' Devil', '')
        season['team'] = season['team'].str.replace('Florida', 'Miami')
        season.to_csv('DATA/season.csv', index = False)


    def get_standings(self):
        dt = datetime.date.today()
        year = dt.year - 1
        win_loss = pd.DataFrame(columns = ['Tm', 'W', 'L', 'W-L%', 'year'])
        while year > 2002:
            url = f'https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml'
            dfs = pd.read_html(url)
            east_al = dfs[0]
            central_al = dfs[1]
            west_al = dfs[2]
            east_nl = dfs[3]
            central_nl = dfs[4]
            west_nl = dfs[5]
            df = pd.concat([east_al, central_al, west_al, east_nl, central_nl, west_nl], ignore_index = True)
            df['year'] = year
            df = df[['Tm', 'W', 'L', 'W-L%', 'year']]
            win_loss = pd.concat([win_loss, df], ignore_index = True)
            year -= 1
        win_loss.columns = ['team', 'wins', 'losses', 'w-l%', 'year']
        self.standings = win_loss

    def get_results(self):
        url = 'https://www.baseball-reference.com/postseason/'
        df = pd.read_html(url)[0]
        df = df.dropna()
        df.columns = ['Series', 'Games', 'Teams']
        df[['year', 'series']] = df['Series'].str.extract(r'(\d+)(.*)')
        df[['series']] = df['series'].str.extract(r'\s*(.*?)(?=\d|$)')
        df['year'] = df['year'].astype('int')
        df = df[df['year'] > 2002]
        df = df[df['year'] < 2023]
        df[['winner']] = df['Teams'].str.extract(r'(.*?)\**\s*\(')
        df[['loser']] = df['Teams'].str.extract(r'vs.\s*(.*?)\**\s*\(')
        df1 = df[['year', 'series', 'winner']]
        df2 = df[['year', 'series', 'loser']]
        df1['result'] = 'won'
        df2['result'] = 'lost'
        df1.columns = ['year', 'series', 'team', 'result']
        df2.columns = ['year', 'series', 'team', 'result']

        data = pd.concat([df1, df2], ignore_index=True)
        order = ['World Series', 'ALCS', 'NLCS', 'ALDS', 'NLDS', 'ALWC', 'NLWC']
        data['series'] = pd.Categorical(data['series'], categories = order)
        data = data.sort_values(by = ['series', 'year'])
        data = data.drop_duplicates(subset = ['team', 'year'], keep = 'first').reset_index(drop = True)
        data['series'] = data['series'].astype('string')
        self.result = data

t = seasons()