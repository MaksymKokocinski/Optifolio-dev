import numpy as np
from datetime import *
from dateutil.relativedelta import relativedelta
from numpy.core.fromnumeric import mean
from requests.api import get
from yahoo_fin.stock_info import *



spolki = ['AMZN','MSFT','AAPL']
three_yrs_ago = date.today() - relativedelta(years=3)
returns = pd.DataFrame()
mean_return = pd.DataFrame()
exc_returns = pd.DataFrame()
for i in spolki:
    price = get_data(ticker=i,start_date=three_yrs_ago,interval="1mo",index_as_date=False)
    price = price[['close','date']]
    new_df = price.diff(axis=0)
    price['diff'] = new_df['close']
    price['shifted'] = price['close'].shift(periods=1)
    price['return'] = price['diff']/price['shifted']
    price.iloc[[-1],[4]] = np.nan
    price.drop([0],inplace=True)
    price.drop(price.tail(1).index,inplace=True)

    returns[i] = price['return']
    
    #tabela średniego zwrotu i średniego rocznego zwrotu
    
print(returns)


mean_return['średni zwrot'] = returns.mean()
mean_return['roczny średni zwrot'] = returns.mean()*12 


    


print(returns)

print(mean_return)