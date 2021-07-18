import requests
import json
import dart_fss as dart

import pandas as pd

def get_csv_corp_info_by_type(api_key, corp_code, type):    
    fs = dart.fs.extract(corp_code=corp_code, bgn_de='20200101', fs_tp=[type], report_tp='annual', lang='ko')
    df = fs[type]
    
    data_idx = 4 if type != 'is' else 3

    # drop columns
    df.drop('concept_id', inplace=True, axis=1, level=1)
    df.drop('label_en', inplace=True, axis=1, level=1)
    df.drop('class0', inplace=True, axis=1, level=1)
    df.drop('class4', inplace=True, axis=1, level=1)

    # manufacturingDataFrame
    long_clm = df.columns[0][0]
    df.rename(columns={long_clm:""}, inplace=True) # Rename Long Columns
    level0 = list(df.columns.get_level_values(0)) # Get 0 level index
    level1 = list(df.columns.get_level_values(1)) # Get 1 level index

    level0[data_idx:] = [ str(x)[:4] for x in level0[data_idx:]] # years
    level1[data_idx:] = ['']*len(level1[data_idx:])

    years = level0[data_idx:]

    level = [str(x) + str(y) for x, y in zip(level0, level1)]
    df.columns = level # Columns

    # add corp_code columns
    df.insert(0, 'corp_code', corp_code)    

    # Get CSV
    col = list(df.columns)[:data_idx + 1]
    print(col)
    for year in years :
        print(">> ", year)

        col_tmp = col + [year]

        df_tmp = df[col_tmp]
        df_tmp.rename(columns={year:"data"}, inplace=True)

        # add year column
        df_tmp.insert(1, 'year', year)

        df_tmp.to_csv("data/{type}_{year}.csv".format(type = type, year = year), sep=",", na_rep="")

# Set API Key
print("[RUN] Setting API key...")
api_key = input("API Key를 입력하세요: ")
dart.set_api_key(api_key=api_key)

# Get Corp List
print("[RUN] Getting Corp List...")
corp_list = dart.get_corp_list()
corps = [*corp_list._corp_codes]

# Get Data
print("[RUN] Getting Data...")
get_csv_corp_info_by_type(api_key, '00126380', 'bs')
get_csv_corp_info_by_type(api_key, '00126380', 'cf')
get_csv_corp_info_by_type(api_key, '00126380', 'is')
