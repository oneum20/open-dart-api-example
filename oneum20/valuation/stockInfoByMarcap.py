from marcap.marcap_utils import marcap_data
import pandas as pd

def get_stocks(stock_code, year):    
    days=range(1,31)
    df = pd.DataFrame()
    for day in days:            
        df = marcap_data("{year}-12-{day}".format(year=year, day=day), code=stock_code)

        df = df.assign(Amount=df['Amount'].astype('int64'),
                    Marcap=df['Marcap'].astype('int64'))

        df.index.name = None
        if not df.empty:         
            print(">>{year}-12-{day}".format(year=year, day=day))   
            break
    return df[['Close','Stocks']]

# years = ['2017','2018','2019','2020']
# for year in years:
#     print("[Get] {} data".format(year))
#     result = get_stocks('005935', year)
#     print(result[['Close','Stocks']])

