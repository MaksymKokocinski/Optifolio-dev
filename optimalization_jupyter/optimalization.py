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
exc_returns = pd.DataFrame()
sharpe_ratio = pd.DataFrame()


portfolio['wartość'] = portfolio['liczba_akcji'] * portfolio['obecny kurs']
portfolio_value=portfolio['wartość'].sum() #aktualna wartość portfolio
portfolio['procent wartosci'] = portfolio['wartość']/portfolio_value #procent wartości danej akcji w całym portfleu
wagi = portfolio['procent wartosci'].to_numpy()

def monthly_returns(companies_list):
    for i in companies_list:
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
    return returns 

returns = monthly_returns(spolki)
sharpe_ratio["sharpe_ratio"] = returns.mean()/returns.std()
#funkcja licząca macierz kowariancji
def variance_covariance_matrix(mean_returns_dataframe):
    mean_return_series = mean_returns_dataframe.squeeze()
    exc_returns = returns.sub(mean_return_series, axis=1)
    exc_returns = exc_returns.to_numpy()
    exc_returns_trans = exc_returns.transpose()
    var_cov = np.matmul(exc_returns_trans,exc_returns)
    var_cov = np.divide(var_cov,exc_returns.shape[0])
    return var_cov


#funkcja która liczy odchylenie standardowe w zależności od wag
def get_portfolio_std_deviation(weights):
    portfolio_standard_deviation = np.sqrt(np.matmul(np.matmul(weights,variance_covariance_matrix(returns.mean())), weights))
    return portfolio_standard_deviation     

#funkcja która liczy oczekiwany zwrot portfolio w zależności od wag
def get_portfolio_exp_return(weights):
    portfolio_exp_return = np.matmul(returns.mean(), weights)
    return portfolio_exp_return

def get_portfolio_sharpe_ratio(weights):
    portfolio_sharpe_ratio = get_portfolio_exp_return(weights)/get_portfolio_std_deviation(weights)
    return portfolio_sharpe_ratio


max_expected_return = max(returns.mean())
min_std_dev = min(returns.std())
max_sharpe_ratio = max(sharpe_ratio['sharpe_ratio'])

# bnds = ((0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None), (0, None))
# cons = ({'type': 'eq', 'fun': lambda x:  sum(x) - 1},
#         {'type': 'ineq', 'fun': lambda x: min_std_dev - get_portfolio_std_deviation(x)})

# result = opt.minimize(get_portfolio_exp_return, wagi, bounds=bnds, constraints=cons)
# print(result)
cons = ({'type': 'eq', 'fun': lambda x:  sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: get_portfolio_exp_return(x) - max_expected_return})

result = opt.minimize(get_portfolio_std_deviation, wagi, constraints=cons)
print(result.x)
print(result.fun)
print(sum(result.x))

