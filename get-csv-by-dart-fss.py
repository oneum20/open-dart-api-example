import requests
import json
import dart_fss as dart

import pandas as pd

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
corp_code = '00126380'
fs = dart.fs.extract(corp_code=corp_code, bgn_de='20200101', fs_tp=['bs'], report_tp='annual', lang='ko')
df = fs['bs']

# Convert DataFrame
## two dimension index -> one dimension index
long_clm = df.columns[0][0]
df.rename(columns={long_clm:""}, inplace=True) # Rename Long Columns
level0 = list(df.columns.get_level_values(0)) # Get 0 level index
level1 = list(df.columns.get_level_values(1)) # Get 1 level index
level1[8:] = ['']*len(level1[8:])

level = [x + y for x, y in zip(level0, level1)]
df.columns = level # Columns

# add corp_code columns
df.insert(0, 'corp_code', corp_code)

# Config Columns
col = list(df.columns[:8])
years = list(df.columns[9:])

# Get CSV
for year in years :
    print(">> ", year)

    col_tmp = col + [year]

    df_tmp = df[col_tmp]
    df_tmp.rename(columns={year:"data"}, inplace=True)

    # add year column
    df_tmp.insert(1, 'year', year)

    df_tmp.to_csv(year + ".csv", sep=",", na_rep="")
