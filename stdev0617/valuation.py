from pykrx import stock
from matplotlib import pyplot as plt

# type은 day, month, year
def getDefaultValuation(start_date, end_date, stock_id, type):
    df = stock.get_market_fundamental_by_date(start_date,end_date,stock_id,type)
    print(df)
    return df

# 미완성. 진행중.
def drawDataFrame(df):

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10,10))
    axes[0][0].get_childredn()

    plt.plot()
    plt.show()

def init():
    start_date = '20100101'
    end_date = '20210628'
    stock_id = '005930'
    type = 'y'
    drawDataFrame(getDefaultValuation(start_date, end_date, stock_id, type))

init()