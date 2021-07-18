from pykrx import stock
import pandas as pd
import FinanceDataReader as fdr
import elasticsearchUtils as esu
import corpInfoByDartFss as cidf
import dart_fss as dart

def get_kospi_list():
    kospi_stock_codes = fdr.StockListing('KOSPI')['Symbol'].values.tolist()
    return kospi_stock_codes

def get_kospi_stock_by_years(bgn_year, end_year):
    print("[RUN] Getting and Pushing Stock Data... ")

    df = pd.DataFrame()
    years = range(bgn_year, end_year + 1)    
    for year in years:              

        days = reversed(range(1, 32))
        for day in days:
            tmp = stock.get_market_cap_by_ticker("{year}12{day}".format(year=year, day=day), market='KOSPI')
            if not tmp.empty:     
                tmp = tmp.reset_index()  
                
                tmp.insert(1, 'year', year)   

                df = pd.concat([df, tmp], join='outer')
                break
    df = df.fillna("")
    print(df.head())
    return df

def insert_stock_data_into_el():
    list = get_kospi_list()

    df = get_kospi_stock_by_years(2017, 2018)

    el = esu.setEl(ip='192.168.35.200', port='9200')

    esu.insert_df_into_el(el, 'stocks', 'stocks', df)

    cidf.set_dart_api_key()
    corp_list = cidf.get_corp_list()
    cnt = 1
    for stock_code in list[28:]:
        print("[RUN] Getting and Pushing Corp Data... ({cnt}/{total})".format(cnt=cnt, total=len(list)))

        types = ['bs', 'cf', 'is']
        for type in types :
            res = cidf.get_corp_info_by_type(corp_list, stock_code, type, '2020')
            if(not res.empty): esu.insert_df_into_el(el, type, type, res)
        
        cnt = cnt + 1




insert_stock_data_into_el()