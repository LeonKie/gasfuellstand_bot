
import numpy as np    
import pandas as pd
from bs4 import BeautifulSoup



def convert_to_xlsx():
    
    with open('Germany.xls') as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'xml')
        writer = pd.ExcelWriter('Germnay.xlsx')
        for sheet in soup.findAll('Worksheet'):
            sheet_as_list = []
            for row in sheet.findAll('Row'):
                sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in row.findAll('Cell')])
            pd.DataFrame(sheet_as_list).to_excel(writer, sheet_name=sheet.attrs['ss:Name'], index=False, header=False)

        writer.save()


def get_tweet_from_df(df):

    fuellstand = float(df.iloc[0,2].replace(",","."))
    date= df.iloc[0,0]
    injection= df.iloc[0,4].replace(",","")
    withdrawal=df.iloc[0,5].replace(",","")
    trend= df.iloc[0,3].replace(",",".")
    injection_capacity= df.iloc[0,7].replace(",","")
    withdrawal_capacity= df.iloc[0,8].replace(",","")
    
    
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
    f"Gas-Fuellstand: \t{progessbar(fuellstand)} {fuellstand}%\n" + \
    f"Gas-Zufuhr: \t{injection} GWh von max. {injection_capacity} GWh\n" + \
    f"Gas-Entnahme: \t{withdrawal} GWh von max. {withdrawal_capacity} GWh"
    
    return tweet
    
    
    

def main():
    convert_to_xlsx()
    df= pd.read_excel('Germnay.xlsx')
    tweet = get_tweet_from_df(df)
    print(tweet)
    return tweet

if __name__ == '__main__':
    main()