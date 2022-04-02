 
import pandas as pd

import datetime
import json
import requests

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

    fuellstand = df.iloc[0,2]
    date= df.iloc[0,0]
    injection= df.iloc[0,4]
    withdrawal=df.iloc[0,5]
    trend= df.iloc[0,3]
    trend_icon= "📈" if float(trend)>0 else "📉"
    injection_capacity= df.iloc[0,7]
    withdrawal_capacity= df.iloc[0,8]
    
    
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
    f"Gas-Fuellstand: \t{progessbar(fuellstand)} {fuellstand:.0f}%\n" + \
    f"Gas-Zufuhr: \t{injection:.2f} GWh von max. {injection_capacity:.2f} GWh\n" + \
    f"Gas-Entnahme: \t{withdrawal:.2f} GWh von max. {withdrawal_capacity:.2f} GWh" + \
    f"\nTrend: \t{trend}% {trend_icon}" 
    
    return tweet
    
    
    

def main():
    api_key = "ENTER_API_KEY_HERE"
    start = datetime.date(2022,1,1).isoformat()
    end = datetime.date(2022,3,31).isoformat()
    
    df = get_gas_data(api_key,start,end)
    tweet = get_tweet_from_df(df)
    print(tweet)
    return tweet

if __name__ == '__main__':
    main()