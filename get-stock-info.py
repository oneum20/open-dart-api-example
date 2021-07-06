import pandas as pd 

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

import matplotlib.pyplot as plt
import seaborn as sns

def get_stock_code_table():
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] 
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)  
    code_df = code_df[['회사명', '종목코드']]  

    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    return code_df

def get_stock_code(corp_name, code_df):
    return code_df.query("name=='{}'".format(corp_name))['code'].to_string(index=False).strip()

def get_stock_info_from_naverfinance(webdriver, corp):
    url = "https://navercomp.wisereport.co.kr/v2/company/c1040001.aspx?cmp_cd={}".format(corp)
    
    webdriver.get(url)
    time.sleep(2) # Wait webdriver.get()

    html = webdriver.page_source

    soup = bs(html, 'html.parser')
    table = soup.select('table')
    table_html = str(table)
    table_df_list = pd.read_html(table_html)
    
    # Get stock info
    df = table_df_list[9]

    # slice df
    df = df.iloc[:10, :6]

    # converting columns
    df.columns = df.columns.str.replace('연간컨센서스보기','') # remove dump string from columns
    df.columns = df.columns.str.replace('\(IFRS연결\)','') # remove dump string from columns
    df.columns = df.columns.str.strip() # remove culumns space

    df = df.replace({'항목':'펼치기 '}, {'항목':''}, regex=True) # remove dump string from values

    df.reset_index() 

    df = df.pivot_table(columns = ['항목'], values = list(df.columns[:]))
    df.columns = df.columns.str.strip() # remove culumns space
    
    print(df)
    return df

# Configure webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options = options)

# Get stock table
code_df = get_stock_code_table()

# Get stock code
tmp_code = get_stock_code("삼성전자", code_df)
data = get_stock_info_from_naverfinance(driver, tmp_code)

# plotting line chart
plt.figure(figsize=(8, 8))
sns.lineplot(data=data, dashes=False)
plt.show()
