import numpy as np
from datetime import *
from dateutil.relativedelta import relativedelta
from requests.api import get
from yahoo_fin.stock_info import *


#print(get_data("AMZN",end_date='01/'))
bla  = date.today()
t = bla.strftime("%d/%m/%Y")

three_yrs_ago = date.today() - relativedelta(years=3)
#print(three_yrs_ago)
test = get_data("msft",start_date=three_yrs_ago, end_date= "03/01/2022", interval="1mo",index_as_date=False)
#print(test)
test = test[['date','close']]

#zrobić tabele zwrotów close z danego miesiąca - close z miesiąca poprzedniego/close z poprzedniego miesiąca 
#wziąć średni zwrot i odchylenie 

new_df = test.diff(axis=0)
test['diff'] = new_df['close']
test['shifted'] = test['close'].shift(periods=1)
test['return'] = test['diff']/test['shifted']
test.iloc[[-1],[4]] = np.nan
mean = test['return'].mean()
annual_mean = mean*12
#print(annual_mean)
annual_std = test['return'].std() *12
std = test['return'].std()
sharpe = annual_mean/annual_std
#print(sharpe)
#print(test)
#tabela 1 - historyczne dane i miesieczne zwroty

spolki = ['AMZN','MSFT','AAPL']
three_yrs_ago = date.today() - relativedelta(years=3)
returns = pd.DataFrame()
for i in spolki:
    price = get_data(ticker=i,start_date=three_yrs_ago,interval="1mo",index_as_date=False)
    price = price[['close','date']]
    new_df = price.diff(axis=0)
    price['diff'] = new_df['close']
    price['shifted'] = test['close'].shift(periods=1)
    price['return'] = price['diff']/price['shifted']
    price.iloc[[-1],[4]] = np.nan
    price.drop([0],inplace=True)
    price.drop(price.tail(1).index,inplace=True)

    returns[i] = price['return']
    


print(returns)