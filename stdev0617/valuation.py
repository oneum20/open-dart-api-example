from pykrx import stock

# type은 day, month, year
def getDefaultValuation(start_date, end_date, stock_id, type):
    df = stock.get_market_fundamental_by_date(start_date,end_date,stock_id,type)
    print(df)

def init():
    start_date = '20100101'
    end_date = '20210628'
    stock_id = '005930'
    type = 'y'
    getDefaultValuation(start_date, end_date, stock_id, type)

init()