from yahoo_fin.stock_info import get_analysts_info, get_data, get_live_price
symbol = "GPW.WA"

test = table = get_data(symbol,start_date="06/05/2020",end_date="06/05/2021",index_as_date=False,interval="1d")

print(test)