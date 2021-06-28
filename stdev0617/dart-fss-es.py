import requests
import json
import dart_fss as dart
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import pandas as pd

def manufacturingDataFrame(fs, tp):
    print('start manufacturingDataFrame..')
    df = fs[tp]

    # 재무제표 열을 연도로 바꾸기
    l = len(df.columns)
    years = []
    for i in range(l-7, l):  # 7부터 마지막 열까지
        year = df.columns[i][0]
        year = year[0:4]
        years.append(year)

    df = removeColumns(df,tp, years)

    return df

def removeColumns(df, tp, years):

    df.columns = df.columns.droplevel()

    df.drop('concept_id', inplace=True, axis=1)
    df.drop('label_en', inplace=True, axis=1)
    df.drop('class0', inplace=True, axis=1)

    if(tp == 'bs'):
        df = df.astype({'label_ko': 'str', 'class1': 'str', 'class2': 'str', 'class3': 'str', 'class4': 'str'})
        class_col = ['label_ko', 'class1', 'class2', 'class3', 'class4']
    elif(tp == 'is'):
        df = df.astype({'label_ko': 'str', 'class1': 'str','class2': 'str'})
        class_col = ['label_ko', 'class1', 'class2']

    elif(tp == 'cf'):
        df = df.astype({'label_ko': 'str', 'class1': 'str','class2': 'str','class3': 'str'})
        class_col = ['label_ko', 'class1', 'class2', 'class3']

    new_col = np.append(class_col, years)
    df.columns = new_col

    df = df.astype({'2020': 'float64', '2019': 'float64', '2018': 'float64', '2017': 'float64', '2016': 'float64', '2015': 'float64','2014': 'float64'})

    df = df.replace(np.NaN, '', regex=True)

    return df

def inputDataIntoES(indexName, df, corp_code):
    es = Elasticsearch(host='10.10.30.182', port=30300)
    es.indices.create(index=indexName)
    documents = df.to_dict(orient='records')
    bulk(es, documents, index=indexName, doc_type=corp_code, raise_on_error=True)
    print('success to input data!!')

def init():
    # Set API Key
    print("[RUN] Setting API key...")
    api_key = input("API Key를 입력하세요: ")
    dart.set_api_key(api_key=api_key)

    # Get Corp List
    print("[RUN] Getting Corp List...")
    # corp_list = dart.get_corp_list()
    # corps = [*corp_list._corp_codes]

    # Get Data
    print("[RUN] Getting Data...")

    corp_code='005930'
    fs = dart.fs.extract(corp_code=corp_code, bgn_de='20170101', report_tp='annual', lang='ko')

    print('start bs..')
    df_bs = manufacturingDataFrame(fs,'bs')
    print(df_bs)
    inputDataIntoES("business_statement",df_bs, corp_code)

    print('start is..')
    df_is = manufacturingDataFrame(fs,'is')
    inputDataIntoES("income_statement", df_is, corp_code)

    print('start cf..')
    df_cf = manufacturingDataFrame(fs,'cf')
    inputDataIntoES("cash_flow_statement", df_cf, corp_code)

init()


