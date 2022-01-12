import numpy as np
import scipy.optimize as opt
from datetime import *
from dateutil.relativedelta import relativedelta
from numpy.core.fromnumeric import mean
from pandas.core.indexes.base import maybe_extract_name
from requests.api import get
from yahoo_fin.stock_info import *



spolki = ['AMZN','MSFT','AAPL']

portfolio = pd.read_csv('test.txt', sep=';')
print(portfolio)
three_yrs_ago = date.today() - relativedelta(years=3)
returns = pd.DataFrame()
mean_return = pd.DataFrame()
mean_std = pd.DataFrame()
exc_returns = pd.DataFrame()
sharpe_ratio = pd.DataFrame()
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
    
#print(returns)


mean_return['średni zwrot'] = returns.mean()

#mean_return['roczny średni zwrot'] = returns.mean()*12 
#print(mean_return)
#mean_return = mean_return.transpose()
mean_return_series = mean_return.squeeze()

#tabela excess zwrotów
exc_returns = returns.sub(mean_return_series, axis=1)
exc_returns = exc_returns.to_numpy()
#print(exc_returns)
exc_returns_trans = exc_returns.transpose()
#print(exc_returns_trans)
#macierz kowariancji pomnożeznie macierzy ex zwrotów z transponowaną nią samą a potem podzielenie przez ilość dat(liczba rzędów tabeli exc return)
#var_cov = exc_returns.mul(exc_returns.transpose())
#print(var_cov)
x = exc_returns.shape[0]
var_cov = np.matmul(exc_returns_trans,exc_returns)
#print(var_cov)
var_cov = np.divide(var_cov,x)
print(var_cov)

#średnie odchylenie
std_dev = pd.DataFrame()
std_dev['std_dev'] = returns.std()
print(std_dev)
sharpe_ratio["sharpe_ratio"] = returns.mean()/returns.std()

print(sharpe_ratio)

portfolio['wartość'] = portfolio['liczba_akcji'] * portfolio['obecny kurs']

#aktualna wartość portfolio
portfolio_value=portfolio['wartość'].sum()

portfolio['procent wartosci'] = portfolio['wartość']/portfolio_value
wagi = portfolio['procent wartosci'].to_numpy()

#portfolio standard deviation
portfolio_std_dev=np.sqrt(np.matmul(np.matmul(wagi,var_cov),wagi))
print('portfolio standard deviation',portfolio_std_dev)

#portfolio expected return
portfolio_exp_return=(returns.mean()*wagi).sum()
prt_2 = np.matmul(returns.mean(),wagi)
print('portfolio eexpected return',portfolio_exp_return, prt_2)

#w tabeli potrzebuje: nazwę firmy, oczekiwane zwroty(na podstawie historii, odchylenie standardowe, wagi) 
#na podstawie oczekiwanych wzrotów /odchylenie standardowe  licze sharpe_ratio dla każdej akcji
new =  pd.DataFrame()
new['name'] = spolki
new['exp_ret'] = mean_return['średni zwrot']
max_expected_return = max(mean_return['średni zwrot'])
min_std_dev = min(returns.std())
#print(returns.std())
#print(min_std_dev)
max_sharpe_ratio = max(sharpe_ratio['sharpe_ratio'])

print(max_expected_return,min_std_dev,max_sharpe_ratio)
print('portfolio sharpe ratio', portfolio_exp_return/portfolio_std_dev)

print('covariance matrix', var_cov)
print('wagi', wagi)

