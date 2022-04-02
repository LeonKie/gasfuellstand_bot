 
import pandas as pd

from datetime import date , timedelta
import json
import requests
import os

def get_gas_data(api_key : str, date_start : str, date_end : str) -> pd.DataFrame:
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

    url = f"https://agsi.gie.eu/api/data/de?from={date_start}&till={date_end}"
    headers = {"x-key": api_key}
    content = requests.request("GET",url, headers=headers)
    gas_data_json = json.loads(content.content)

    df = pd.DataFrame.from_dict(gas_data_json)
    dict_columns_type = {'status': str,
                    'gasDayStartedOn': str,
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
    return df.astype(dict_columns_type)

def get_tweet_from_df(df):

    fuellstand = df.iloc[0,3]
    date= df.iloc[0,1]
    injection= df.iloc[0,5]
    withdrawal=df.iloc[0,6]
    trend= df.iloc[0,4]
    trend_icon= "📈" if float(trend)>0 else "📉"
    injection_capacity= df.iloc[0,8]
    withdrawal_capacity= df.iloc[0,9]
    
    
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
    api_key = os.getenv("AGSI_API_KEY")
    DATE=date.today()
    end=DATE.strftime('%Y-%m-%d')
    start= DATE-timedelta(days=30)
    start=start.strftime('%Y-%m-%d')
    
    
    df = get_gas_data(api_key,start,end)
    
    print(df)
    tweet = get_tweet_from_df(df)
    print(tweet)
    return tweet

if __name__ == '__main__':
    main()