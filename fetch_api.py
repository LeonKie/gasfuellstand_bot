import requests
from datetime import date ,timedelta

def main():
    DATE=date.today()
    today=DATE.strftime('%Y-%m-%d')
    yesterday= DATE-timedelta(days=30)
    yesterday=yesterday.strftime('%Y-%m-%d')
    
    r = requests.get("https://agsi.gie.eu/api/historical-facility-reports-xml/SSO/DE_/"+yesterday+"/"+today+"/Germany.xls")
    with open('Germany.xls', 'wb') as f:
        f.write(r.content)  # write binary data


if __name__ == "__main__":
    main()