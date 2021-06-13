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
fs = dart.fs.extract(corp_code='00126380', bgn_de='20170101', fs_tp=['bs'], report_tp='annual', lang='ko')
print(fs['bs'])
