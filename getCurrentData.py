
import numpy as np    
import pandas as pd
from bs4 import BeautifulSoup

import locale


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


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
    fuellstand= locale.atof(df.iloc[0,2])
    date= df.iloc[0,0]
    injection=locale.atof(df.iloc[0,4])
    withdrawal=locale.atof(df.iloc[0,5])
    trend= locale.atof(df.iloc[0,3])
    injection_capacity= locale.atof(df.iloc[0,7])
    withdrawal_capacity= locale.atof(df.iloc[0,8])

    def progessbar(fuellstand):
        bar=''
        maxchars= 10
        fuellstand_int= int(fuellstand/100*maxchars)
        for i in range(0,maxchars):
            if i<=fuellstand_int:
                bar+='▓▓'
            else:
                bar+='░░'
        return bar
    
    tweet= "Automatisiert - Stand: "+ date +" \n" +"Gas-Fuellstand: " + progessbar(fuellstand) + " "+str(fuellstand) + "%,\n"\
        + ", " + " Gas-Injection:" +  str(injection) + "GWh, " + str(withdrawal) + "GWh, " + str(trend)
    
    #print(tweet)
    
    
    

def main():
    convert_to_xlsx()
    df= pd.read_excel('Germnay.xlsx')
    tweet = get_tweet_from_df(df)
    
    return tweet

if __name__ == '__main__':
    main()