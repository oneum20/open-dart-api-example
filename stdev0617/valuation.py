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

def init():
    start_date = '20100101'
    end_date = '20210628'
    stock_id = '005930'
    type = 'y'
    drawDataFrame(getDefaultValuation(start_date, end_date, stock_id, type))

init()