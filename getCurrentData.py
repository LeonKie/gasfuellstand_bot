 
import pandas as pd

from datetime import date , timedelta
import json
import requests
import os

def get_gas_data(date_start : str, date_end : str):
    """
    Parameters:
    api_key : str
        api_key for AGSI+
    date_start : str
        date in YYYY-MM-DD format 
    date_end : str
        date in YYYY-MM-DD format

    Returns:
        Pandas dataframe

    """
    
    url = f"https://agsi.gie.eu/api?country=DE&from={date_start}&to={date_end}&page=1&size=5"
    
    api_key=  os.getenv("AGSI_API_KEY"),
    
    print(url)
    headers = {"x-key": str(api_key)}
    #content = requests.get(url, headers=headers)
    content = requests.request("GET",url, headers=headers)
    
    gas_data_json = json.loads(content.content)
    gas_data_json= gas_data_json['data'][-1]
    print(gas_data_json)
    #df = pd.DataFrame.from_dict(gas_data_json)
    '''
    dict_columns_type = {'status': str,
                    'gasDayStart': str,
                    'gasInStorage': float,
                    'full': float,
                    'trend': float,
                    'injection': float,
                    'injectionCapacity': float,
                    'withdrawal': float,
                    'withdrawalCapacity': float,
                    'workingGasVolume': float,
                    'info': str
                }
    '''
    #return df.astype(dict_columns_type)
    
    return gas_data_json
    

def get_tweet_from_df(df):

    fuellstand = float(df['full'])
    date= df['gasDayStart']
    injection= float(df['injection'])
    withdrawal= float(df['withdrawal'] )
    trend= float(df['trend'])
    trend_icon= "📈" if float(trend)>0 else "📉"
    injection_capacity= float(df['injectionCapacity'])
    withdrawal_capacity= float(df['withdrawalCapacity'])
    
    
    def progessbar(fuellstand):
        bar=''
        maxchars= 6
        fuellstand_int= int(fuellstand/100*maxchars)
        for i in range(0,maxchars):
            if i<=fuellstand_int:
                bar+='▓▓'
            else:
                bar+='░░'
        return bar
    
    tweet = f"Stand: \t{date} \n"+ \
    f"Gas-Fuellstand: \t{progessbar(fuellstand)} {fuellstand:.2f}%\n" + \
    f"Gas-Zufuhr: \t{injection:.2f} GWh von max. {injection_capacity:.2f} GWh\n" + \
    f"Gas-Entnahme: \t{withdrawal:.2f} GWh von max. {withdrawal_capacity:.2f} GWh" + \
    f"\nTrend: \t{trend:.2f}% {trend_icon}" 
    
    return tweet
    
    
    

def main():
    DATE=date.today()
    end=DATE.strftime('%Y-%m-%d')
    start= DATE-timedelta(days=5)
    start=start.strftime('%Y-%m-%d')
    
    
    df = get_gas_data(start,end)
    
    print(df)
    tweet = get_tweet_from_df(df)
    print(tweet)
    return tweet

if __name__ == '__main__':
    main()