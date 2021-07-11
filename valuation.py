import pandas as pd
import numpy as np

import dart_fss as dart

import matplotlib.pyplot as plt
import seaborn as sns

from elasticsearch import Elasticsearch
import stockInfoByMarcap as sim


def get_info_by_corp_code(es, corp_code, index, attr, value, year):
    index = index
    body = {    
        'size':10000,
        'query':{
            "bool":{
                "should": [
                    {
                        "match":{
                            "corp_code":corp_code
                        }
                    },
                    {
                        "match":{
                            "year":year
                        }
                    },
                    {
                        "match":{
                            attr:value
                        }
                    }
                ]
            }
                
        }
    }
    data = es.search(index=index, body=body)
    return int(data['hits']['hits'][0]['_source']['data'])

def valuate(corp_code, stock_code, str_year, end_year):
    res = pd.DataFrame()

    years = range(str_year, end_year + 1)
    for year in years:
        year = str(year)

        df = sim.get_stocks(stock_code, year) # get Stocks & Close
        stocks = int(df['Stocks'].to_string(index=False).strip())
        close = int(df['Close'].to_string(index=False).strip())

        # Get PER
        dks = get_info_by_corp_code(es, corp_code, 'is', 'label_ko', '당기순이익(손실)', year)

        eps = dks/stocks
        per = close/eps
        # print("PER : {}".format(per))

        # Get PBR (주가/bps)
        tteq = get_info_by_corp_code(es, corp_code, 'bs', 'label_ko', '자산총계', year)
        ttdb = get_info_by_corp_code(es, corp_code, 'bs', 'label_ko', '부채총계', year)
        eq = tteq - ttdb

        bps = eq/stocks
        pbr = close/bps
        # print("PBR : {}".format(pbr))

        # Get PCR
        cashflow = get_info_by_corp_code(es, corp_code, 'cf', 'label_ko', '영업활동 현금흐름', year)

        cps = cashflow/stocks
        pcr = close/cps
        # print("PCR : {}".format(pcr))

        # Get PSR 
        sales = get_info_by_corp_code(es, corp_code, 'is', 'label_ko', '수익(매출액)', year)

        sps = sales/stocks
        psr = close/sps
        # print("PSR : {}".format(psr))

        record = {
            stock_code:{
                'year':year,
                'per':per,
                'pbr':pbr,
                'pcr':pcr,
                'psr':psr
            }
        }
        res = pd.concat([res, pd.DataFrame(record, index=['year','per','pbr','pcr','psr']).T], join='outer')
    print(res)
    return res.astype({'per':'float64','pbr':'float64','pcr':'float64','psr':'float64'})

        
# Setting open dart api
api_key=input("api key를 입력하세요: ")
dart.set_api_key(api_key=api_key)

# Get corp info
corp = dart.get_corp_list().find_by_corp_name('삼성전자', exactly=True)[0]
corp_code = corp.corp_code
stock_code = corp.stock_code

# Setting ElasticSearch
ip = '192.168.35.200'
port = '9200'
es = Elasticsearch(host=ip, port=port)

# Get stock info
year = '2017'

df = valuate(corp_code=corp_code, stock_code=stock_code, str_year=2017, end_year=2019)

df = df.melt('year', var_name='cols',  value_name='vals')
g = sns.lineplot(x="year", y="vals", hue='cols', data=df)
plt.show()






