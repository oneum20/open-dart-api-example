# dart_fss
import dart_fss as dart

# rest api
import requests
import json

# util
from time import sleep
import pandas as pd

api_key=input("api key를 입력하세요: ")
dart.set_api_key(api_key=api_key)

# Get all corp list
CorpList = dart.corp.get_corp_list()


codes = list(CorpList._corp_codes.keys())
items=codes[86925:86935]
items

j = 0
url = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
table = pd.DataFrame()
for i in items :
    print(">> ", j, "/", len(items))
    req_data = {'crtfc_key':api_key, 'corp_code':i, 'bsns_year' : '2017', 'reprt_code':'11011'}
    res = json.loads(requests.get(url, params=req_data).text)
    if res['status'] == '000' :   
        df = pd.DataFrame(res['list'])
        df2 = df[ df['fs_div'] == 'CFS']
        tmp = df2[['corp_code','account_nm', 'thstrm_amount']].pivot_table(index = 'corp_code', columns = ['account_nm'], values = 'thstrm_amount', aggfunc='first')
        print(type(table), "|", type(tmp))
        print(tmp)
        if not tmp.empty : 
            table = pd.concat([table, tmp], join='outer')
    else :
        print(res['message'])

    sleep(1)
    j += 1

print("RES:: ")
print(table)
