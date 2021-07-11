from pykrx import stock
from matplotlib import pyplot as plt
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import FinanceDataReader as fdr
import OpenDartReader
from pandas import Series, DataFrame

# type은 day, month, year
def getDefaultValuation(start_date, end_date, stock_id, type):
    df = stock.get_market_fundamental_by_date(start_date,end_date,stock_id,type)
    print(df)
    return df

# 미완성. 진행중.
def drawDataFrameFromAPI(df):

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,10))
    plt.subplots_adjust(hspace=0.35,wspace=0.5) # subplot 간의 간격 조절 (hspace는 위/아래, wspace는 왼쪽/오른쪽)
    bps_series = df['BPS']
    per_series = df['PER']
    pbr_series = df['PBR']
    eps_series = df['EPS']
    div_series = df['DIV']
    dps_series = df['DPS']

    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[0][2]
    ax3 = axes[1][0]
    ax4 = axes[1][1]
    ax5 = axes[1][2]

    ax0.plot(bps_series.index, bps_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax0.set_title('Samsung BPS', fontsize=10, family='Arial');
    _ = ax0.set_ylabel('BPS', fontsize=10, family='Arial');
    _ = ax0.set_xlabel('date', fontsize=10, family='Arial');
    ax0.legend(loc="upper left");

    ax1.plot(eps_series.index, per_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax1.set_title('Samsung PER', fontsize=10, family='Arial');
    _ = ax1.set_ylabel('PER', fontsize=10, family='Arial');
    _ = ax1.set_xlabel('date', fontsize=10, family='Arial');
    ax1.legend(loc="upper left");

    ax2.plot(eps_series.index, pbr_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax2.set_title('Samsung PBR', fontsize=10, family='Arial');
    _ = ax2.set_ylabel('PBR', fontsize=10, family='Arial');
    _ = ax2.set_xlabel('date', fontsize=10, family='Arial');
    ax2.legend(loc="upper left");

    ax3.plot(bps_series.index, eps_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax3.set_title('Samsung EPS', fontsize=10, family='Arial');
    _ = ax3.set_ylabel('EPS', fontsize=10, family='Arial');
    _ = ax3.set_xlabel('date', fontsize=10, family='Arial');
    ax3.legend(loc="upper left");

    ax4.plot(bps_series.index, div_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax4.set_title('Samsung DIV', fontsize=10, family='Arial');
    _ = ax4.set_ylabel('DIV', fontsize=10, family='Arial');
    _ = ax4.set_xlabel('date', fontsize=10, family='Arial');
    ax4.legend(loc="upper left");

    ax5.plot(bps_series.index, dps_series, linewidth=2, linestyle='-', label="BPS");
    _ = ax5.set_title('Samsung DPS', fontsize=10, family='Arial');
    _ = ax5.set_ylabel('DPS', fontsize=10, family='Arial');
    _ = ax5.set_xlabel('date', fontsize=10, family='Arial');
    ax5.legend(loc="upper left");
    fig.suptitle("<Samsung>", fontsize=10, family='Verdana')

    plt.show()

def drawValuation():
    df = makeDataFrameForValuation()

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
    plt.subplots_adjust(hspace=0.35,wspace=0.5) # subplot 간의 간격 조절 (hspace는 위/아래, wspace는 왼쪽/오른쪽)

    ax0 = axes[0][0]
    ax1 = axes[0][1]
    ax2 = axes[1][0]
    ax3 = axes[1][1]

    ax0.plot(df['PER'].index, df['PER'], linewidth=2, linestyle='-', label="PER");
    _ = ax0.set_title('PER', fontsize=10, family='Arial');
    _ = ax0.set_ylabel('PER', fontsize=10, family='Arial');
    _ = ax0.set_xlabel('date', fontsize=10, family='Arial');
    ax0.legend(loc="upper left");

    ax1.plot(df['PBR'].index, df['PBR'], linewidth=2, linestyle='-', label="PBR");
    _ = ax1.set_title('PBR', fontsize=10, family='Arial');
    _ = ax1.set_ylabel('PBR', fontsize=10, family='Arial');
    _ = ax1.set_xlabel('date', fontsize=10, family='Arial');
    ax1.legend(loc="upper left");

    ax2.plot(df['PCR'].index, df['PCR'], linewidth=2, linestyle='-', label="PCR");
    _ = ax2.set_title('PCR', fontsize=10, family='Arial');
    _ = ax2.set_ylabel('PCR', fontsize=10, family='Arial');
    _ = ax2.set_xlabel('date', fontsize=10, family='Arial');
    ax2.legend(loc="upper left");

    ax3.plot(df['PSR'].index, df['PSR'], linewidth=2, linestyle='-', label="PSR");
    _ = ax3.set_title('PSR', fontsize=10, family='Arial');
    _ = ax3.set_ylabel('PSR', fontsize=10, family='Arial');
    _ = ax3.set_xlabel('date', fontsize=10, family='Arial');
    ax3.legend(loc="upper left");

    fig.suptitle("<Samsung>", fontsize=10, family='Verdana')

    plt.show()

def getESData(index_name, attr, value):
    es = Elasticsearch(host='10.10.30.182', port=30300)

    result = es.search(index=index_name, body = {
        "query":
            {
                "match":
                    {
                        attr: value
                    }
            }
    })
    return result

def getKOSPIList():
    df_krx = fdr.StockListing('KRX')

    df_KOSPI = df_krx[df_krx['Market']=='KOSPI']
    print(len(df_KOSPI))

    KOSPI = list(df_KOSPI['Symbol'])
    print(KOSPI)

def makeDataFrameForValuation():
    years = ['2017','2018','2019','2020']
    corp_code = '005930'
    total_2017 = getMarketCap(corp_code, '2017-12-28')
    total_2018 = getMarketCap(corp_code, '2018-12-28')
    total_2019 = getMarketCap(corp_code, '2019-12-30')
    total_2020 = getMarketCap(corp_code, '2020-12-30')

    raw_data = {'PER': [getPER(corp_code, total_2017, '2017-12-28'), getPER(corp_code, total_2018, '2018-12-28'), getPER(corp_code, total_2019, '2019-12-30'), getPER(corp_code, total_2020, '2020-12-30')],
            'PBR': [getPBR(corp_code, total_2017, '2017-12-28'), getPBR(corp_code,total_2018,'2018-12-28'), getPBR(corp_code,total_2019, '2019-12-30'), getPBR(corp_code,total_2020,'2020-12-30')],
            'PCR': [getPCR(corp_code, total_2017, '2017-12-28'), getPCR(corp_code,total_2018,'2018-12-28'), getPCR(corp_code,total_2019, '2019-12-30'), getPCR(corp_code,total_2020,'2020-12-30')],
            'PSR': [getPSR(corp_code, total_2017, '2017-12-28'), getPSR(corp_code,total_2018,'2018-12-28'), getPSR(corp_code,total_2019, '2019-12-30'), getPSR(corp_code,total_2020,'2020-12-30')]}
    data = DataFrame(raw_data, index=years)
    return data

def getCloseData(corp_code, start_date, end_date):
    df = fdr.DataReader(corp_code, start_date, end_date)
    return int(df['Close'].get(start_date))

def getMarketCap(corp_code, date):
    df = stock.get_market_cap_by_ticker(date.replace('-',''))
    return int(df['시가총액'].get(corp_code))

def getEarning(year):
    data = getESData("income_statement", "class1", "당기순이익(손실)")
    return int(data['hits']['hits'][0]['_source'][year])

def getSales(year):
    data = getESData("income_statement", "class1", "수익(매출액)")
    return int(data['hits']['hits'][0]['_source'][year])

def getCashflow(year):
    data = getESData("cash_flow_statement", "label_ko", "영업활동 현금흐름")
    return int(data['hits']['hits'][0]['_source'][year])

def getPER(corp_code, total, date):
    year = date[:4]
    # return getCloseData(corp_code, date, date) * getCountOfIssuedStock(corp_code, date) / getEarning(year)
    return total / getEarning(year)

def getPBR(corp_code, total, date):
    year = date[:4]
    assets = int(getESData("business_statement", "class2", "자산총계")['hits']['hits'][0]['_source'][year])
    liabilities = int(getESData("business_statement", "class2", "부채총계")['hits']['hits'][0]['_source'][year])
    # return getCloseData(corp_code, date, date) * getCountOfIssuedStock(corp_code, date) / (assets - liabilities);
    return total / (assets - liabilities);

def getPSR(corp_code, total, date):
    year = date[:4]
    # return getCloseData(corp_code, date, date) * getCountOfIssuedStock(corp_code, date) / getSales(year)
    return total / getSales(year)

def getPCR(corp_code, total, date):
    year = date[:4]
    # return getCloseData(corp_code, date, date) * getCountOfIssuedStock(corp_code, date) / getCashflow(year)
    return total / getCashflow(year)

def printValuation(corp_code, date):
    print('PER: ', getPER(corp_code, date))
    print('PBR: ', getPBR(corp_code, date))
    print('PSR: ', getPSR(corp_code, date))
    print('PCR: ', getPCR(corp_code, date))

def init():
    start_date = '20201230'
    end_date = '20201230'
    corp_code = '005930'

    # print("[RUN] Setting API key...")
    # api_key = input("API Key를 입력하세요: ")
    # dart_obj = OpenDartReader(api_key)

    type = 'y'
    # drawDataFrame(getDefaultValuation(start_date, end_date, stock_id, type))
    # getESData()
    # PER = getStockData(stock_id, start_date, end_date)
    # getCountOfIssuedStock(stock_id, dart_obj)
    # getEarning()

    # print(getPER(dart_obj, corp_code, '2019-12-30'))
    # print(getPER(dart_obj, corp_code, '2018-12-28'))
    # print(getPER(dart_obj, corp_code, '2017-12-30'))
    # printValuation(corp_code, '2020-12-30')
    drawValuation()

init()