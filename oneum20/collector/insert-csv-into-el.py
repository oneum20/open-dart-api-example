import pandas as pd 
import numpy as np

import elasticsearchUtils as esu

import config

def insert_fs_to_el(bgn_year, end_year):
    print("[RUN] Starting...")
    years = range(bgn_year, end_year + 1)
    types = ['bs', 'cf', 'is']
    for year in years:
        for type in types:  
            print("[RUN] {} :: Getting CSV file...".format(year))      

            path = config.CONFIG['collector']['path'] + "/{type}/{year}_fs_{type}.csv".format(type=type, year=year)
            print("\t\t>> FILE NAME : {}".format(path))

            # Get Data
            df = pd.read_csv(path, delimiter="\t").replace(np.NaN, '', regex=True).iloc[:,1:] # CSV 가져오기
            df['종목코드'] = df['종목코드'].str.strip('[]') # 종목코드 괄호 제거

            df.insert(1, '연도', year)
            
            esu.insert_df_into_el(esu.setEl(config.CONFIG['el-server']['ip'], config.CONFIG['el-server']['port']),
                                data=df,
                                index=type,
                                type=type) 
