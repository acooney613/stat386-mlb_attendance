import pandas as pd
import datetime

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
        self.pay['team'] = self.pay['team'].str.replace('Oakland Athletics', 'Oakland A’s')
        self.pay['team'] = self.pay['team'].str.replace('Indians', 'Guardians')
        self.pay.to_csv('DATA/payroll.csv', index = False)
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