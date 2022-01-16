from xml.dom import NoDataAllowedErr
import pandas as pd
import numpy as np
import scipy.optimize as opt
from decimal import Context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import CreateUserForm, CustomerForm, AddSharesForm, AddPortfolioForm
from .decorators import unauthenticated_user,allowed_users,admin_only

from django.db.models import Count, Sum, F

from datetime import *
from dateutil.relativedelta import relativedelta
from yahoo_fin.stock_info import get_analysts_info, get_data, get_live_price
#from . import csv_reader

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'optifolio/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('summary')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {}
    return render(request, 'optifolio/login.html', context)    

def logoutUser(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    context = {}
    return render(request, 'optifolio/userpage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('summary') 


    context = {'form':form}
    return render(request, 'optifolio/account_settings.html',context)



@unauthenticated_user
def homepage(request):
    context = {}
    return render(request, 'optifolio/homepage.html', context)


@login_required(login_url='homepage')
@admin_only
def adminpage(request):
    context = {}
    return render(request, 'optifolio/adminpage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer(request, pk):
    customer = Customer.objects.get(id = pk)
    
    #global customer pk
    customer_pk = int(customer.pk)

    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('summary') 

    context = {'customer':customer,'form':form,'customer_pk':customer_pk}
    return render(request, 'optifolio/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id = pk)
    if request.method == "POST":
        customer.delete()
        return redirect('homepage')

    context = {'item': customer}
    return render(request, 'optifolio/delete_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def visualisationPage(request):
    current_user_name = request.user.customer
    
    form = AddSharesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            publish = form.save(commit=False)
            publish.user_name = current_user_name #Adding username to form
            publish.save()
            return redirect('visualisationpage')
    else:
            form = AddSharesForm()

    #for user restriction 

    # tutaj trzeba to uzaleznic od nr portfolio
    visdata = request.user.customer.visdata_set.all()

    #tu sobie licze obecna zawartosc portfolio
    portfolio_current_state = {}
    for tr in visdata:
        print(tr.title2)
        if tr.title2 in portfolio_current_state:
            print('jest')
            # wtedy dodaj liczbe akcji do tych co byly wczesniej (lub odejmij jesli sell)
        else:
            print('niema')
            portfolio_current_state[tr.title2] = [tr.shares_number]
        print(portfolio_current_state)


    price = []
    for v in visdata:
        #print(v.title2)
        price.append(get_live_price(str(v.title2)))

    '''visdata = request.user.customer.visdata_set.all()
    count_visdata = visdata.count()
    price = []
    if count_visdata > 0:
        for temporary in range(count_visdata):
            price.append(get_live_price(str(visdata[temporary])))            
    else:
        price = []'''
    
    context = {'form': form, 'visdata':visdata,'current_user_name':current_user_name, 'price':price}
    return render(request, 'optifolio/visualisationpage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def addVisData(request, pk):
    current_user_name = request.user.customer
    current_portfolio = Portfolio.objects.get(portfolio_id = pk)
    visdata = current_portfolio.visdata_set.all()

    form = AddSharesForm(request.POST or None)
    if request.method == 'POST':
        #print(form.data)
        if form.is_valid():
            #print(form.cleaned_data)
            publish = form.save(commit=False)
            publish.user_name = current_user_name
            
            publish.portfolio_name = current_portfolio
            publish.save()
            return redirect('vispage', pk)
    else:
            form = AddSharesForm()


    context = {'form': form, 'current_user_name':current_user_name, 'portfolio_pk': pk}
    return render(request, 'optifolio/add_transaction.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateVisData(request, pk, vispk):
    transaction = VisData.objects.get(visdata_id=vispk)
    form = AddSharesForm(instance=transaction)

    if request.method == 'POST':
        form = AddSharesForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('vispage', pk)

    context = {'form': form, 'vispk': vispk, 'pk':pk}
    return render(request, 'optifolio/update_transaction.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteVisData(request, pk, vispk):
    transaction = VisData.objects.get(visdata_id=vispk)
    if request.method == "POST":
        transaction.delete()
        return redirect('vispage', pk)
    context = {'item': transaction, 'vispk': vispk, 'pk':pk}
    return render(request, 'optifolio/delete_transaction.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def summaryPage(request):
    current_user_name = request.user.customer
    visdata = request.user.customer.visdata_set.all()
    all_user_portfolio = request.user.customer.portfolio_set.all()


    count_portfolio = all_user_portfolio.count()
    '''if count_portfolio > 0:
        #print('test2',count_portfolio,all_user_portfolio)
        for temp in range (count_portfolio):
            print(all_user_portfolio[temp])'''

    #Every user can have only 3 portfolios top
    if count_portfolio < 3:
        form = AddPortfolioForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                publish = form.save(commit=False)
                publish.user_name = current_user_name #Adding username to form
                publish.save()
                return redirect('summary')
        else:
            form = AddPortfolioForm()
    else:
        form = AddPortfolioForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                publish = form.save(commit=False)
                return redirect('summary')
                
    
    context = {'form':form,'all_user_portfolio':all_user_portfolio,}
    return render(request, 'optifolio/summary.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deletePortfolio(request, pk):
    portfolio = Portfolio.objects.get(portfolio_id=pk)
    if request.method == "POST":
        portfolio.delete()
        return redirect('summary')
    context = {'item': portfolio}
    return render(request, 'optifolio/delete_portfolio.html', context)
  
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def visPage(request, pk):
    current_user_name = request.user.customer
    current_portfolio = Portfolio.objects.get(portfolio_id = pk)
    visdata = current_portfolio.visdata_set.all()

    # Popup z formularzem pozwalającym usunąć transakcję
    '''form = DeletePortfolioForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            publish = form.save(commit=False)
            publish.user_name = current_user_name #Adding username to form
            publish.save()
            return redirect('summary')
    else:
        form = AddPortfolioForm()'''


    price = []
    for v in visdata:
        price.append(get_live_price(str(v.title2)))
        
    comp_number = visdata.count()
    if comp_number > 0:
        
        shares_num = visdata.aggregate(Sum(('shares_number')))
        shares_num_sum = (shares_num['shares_number__sum'])
        shares_num_sum = format(shares_num_sum, ".0f")
        fare_paid = visdata.aggregate(Sum(('fare')))
        fare_sum = (fare_paid['fare__sum'])
        mod_date = visdata.order_by('-date').first().date
        to_buy = visdata.filter(buy_sell='+').count()
        to_sell = visdata.filter(buy_sell='-').count()
        to_buy_percentage = 0
        to_buy_percentage = to_buy / comp_number
        to_buy_percentage = (to_buy_percentage) * 100
        to_buy_percentage = format(to_buy_percentage, ".0f")
        to_buy_percentage = str(to_buy_percentage) + '%'
        
        aggregated_data = visdata.annotate(
        intermid_result=F('course') - F('fare') 
        ).annotate(
        record_total=F('shares_number') * F('intermid_result')
        ).aggregate(
        total=Sum('record_total')
        )
        profit_earned = aggregated_data['total']
        profit_earned = format(profit_earned, ".2f")
        
        current_portfolio = Portfolio.objects.get(portfolio_id = pk)
        current_portfolio.p_shares_num_sum = shares_num_sum
        current_portfolio.p_comp_num_sum = comp_number
        current_portfolio.p_last_mod_date = mod_date
        current_portfolio.p_profit_earned = profit_earned
        current_portfolio.p_to_buy_percentage = to_buy_percentage
        current_portfolio.save()

        print('smthSssssss',current_portfolio.p_shares_num_sum,current_portfolio.p_to_buy_percentage,current_portfolio.p_comp_num_sum ,current_portfolio.p_last_mod_date,current_portfolio.p_profit_earned)

    else:
        shares_num_sum = 0
        fare_sum = 0
        mod_date = 'brak'
        to_buy = 0
        to_sell = 0
        to_buy_percentage = 0
        profit_earned = 0
    

    context = {'current_portfolio':current_portfolio, 'visdata':visdata,'current_user_name':current_user_name,'price':price}
    return render(request, 'optifolio/vispage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def portfolioState(request, pk):
    current_user_name = request.user.customer
    current_portfolio = Portfolio.objects.get(portfolio_id = pk)
    visdata = current_portfolio.visdata_set.all()

    #testowa lista
    #test_list = [['symbol0', 10], ['symbol1', 15], ['symbol2', 20]]

    def get_index_of_sublist(nested_list, element):
        for idx in range(len(nested_list)):
            if nested_list[idx][0] == element:
                return idx
            else:
                idx += 1
        return False

    #nowy kod z obecna zawartoscia portfolio w postaci listy list
    portfolio_current_state = []
    for tr in visdata:
        quantity = tr.shares_number
        #zamieniam dane tak żeby zawsze były floatem
        if quantity is None:
            quantity = 0.0
        else:
            quantity = float(quantity)
        #podliczam liczbę akcji dla kolejnych firm
        if tr.title2 in (item for sublist in portfolio_current_state for item in sublist):
            if tr.buy_sell == '+':
                print('in list and buy')
                idx = get_index_of_sublist(portfolio_current_state, tr.title2)
                if idx:
                    portfolio_current_state[idx][1] += quantity
            elif tr.buy_sell == '-':
                print('in list and sell')
                idx = get_index_of_sublist(portfolio_current_state, tr.title2)
                if idx:
                    portfolio_current_state[idx][1] -= quantity
        else:
            if tr.buy_sell == '+':
                portfolio_current_state.append([tr.title2, quantity])
            elif tr.buy_sell == '-':
                portfolio_current_state.append([tr.title2, -1.0 * quantity])
    #sprawdzam czy liczba akcji dla jakiejś firmy wynosi 0 (i wtedy się jej pozbywam)
    for sub_list in portfolio_current_state:
        if sub_list[1] == 0:
            portfolio_current_state.remove(sub_list)


    price = []
    value = []

    for sub_list in portfolio_current_state:
        price.append(get_live_price(str(sub_list[0])))
        
    for temp in range(len(portfolio_current_state)):
        value.append(portfolio_current_state[temp][1] * price[temp])

    #stary kod ze słownikiem
    #tu sobie licze obecna zawartosc portfolio
    '''portfolio_current_state = {}
    for tr in visdata:
        quantity = tr.shares_number
        #zamieniam dane tak żeby zawsze były floatem
        if quantity is None:
            quantity = 0.0
        else:
            quantity = float(quantity)
        #podliczam liczbę akcji dla kolejnych firm
        if tr.title2 in portfolio_current_state:
            if tr.buy_sell == '+':
                portfolio_current_state[tr.title2] += quantity
            elif tr.buy_sell == '-':
                portfolio_current_state[tr.title2] -= quantity
        else:
            if tr.buy_sell == '+':
                portfolio_current_state[tr.title2] = quantity
            elif tr.buy_sell == '-':
                portfolio_current_state[tr.title2] = -1.0 * quantity
    #sprawdzam czy liczba akcji dla jakiejś firmy wynosi 0 (i wtedy się jej pozbywam)
    for k in list(portfolio_current_state.keys()):
        if portfolio_current_state[k] == 0:
            del portfolio_current_state[k]

        #print(portfolio_current_state)'''

    #przesylam portfolio current state do podstronki z optymalizacja
    request.session['portfolio_current_state'] = portfolio_current_state

    context = {'portfolio_current_state': portfolio_current_state, 'visdata': visdata, 'current_portfolio': current_portfolio,'price':price,'value':value,}
    return render(request, 'optifolio/portfolio_state.html', context)


#Zuza tu funkcja do twojej stronki
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def portfolioOptimize(request, pk):
    current_user_name = request.user.customer
    current_portfolio = Portfolio.objects.get(portfolio_id = pk)
    visdata = current_portfolio.visdata_set.all()

    # odbieram portfolio current state z podstronki z obecnym stanem portfolio
    portfolio_current_state = request.session.get('portfolio_current_state')

    def Extract(lst):
        return [item[0] for item in lst]

    spolki = Extract(portfolio_current_state)
    portfolio = pd.DataFrame(portfolio_current_state,index=spolki, columns=['spolki','ilosc akcji'])
    #portfolio = pd.DataFrame.from_dict(portfolio_current_state, orient='index',columns=['ilosc akcji'])
    price = []
    for index,row in portfolio.iterrows():
        price.append(get_live_price(str(index)))
    portfolio['live price'] = price
    print(portfolio)

    three_yrs_ago = date.today() - relativedelta(years=3)
    returns = pd.DataFrame()
    exc_returns = pd.DataFrame()
    sharpe_ratio = pd.DataFrame()

    portfolio['wartość'] = portfolio['ilosc akcji'] * portfolio['live price']
    portfolio_value=portfolio['wartość'].sum() #aktualna wartość portfolio
    
    portfolio['procent wartosci'] = portfolio['wartość']/portfolio_value
    wagi = portfolio['procent wartosci'].to_numpy()
    print(portfolio)
    print(wagi)


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

    #spolki = portfolio_current_state.keys()
    returns = monthly_returns(spolki)
    sharpe_ratio["sharpe_ratio"] = returns.mean()/returns.std()
    
    #funkcja licząca macierz kowariancji
    def variance_covariance_matrix(mean_returns_dataframe):
        mean_return_series = mean_returns_dataframe.mean().squeeze()
        exc_returns = mean_returns_dataframe.sub(mean_return_series, axis=1)
        exc_returns = exc_returns.to_numpy()
        exc_returns_trans = exc_returns.transpose()
        var_cov = np.matmul(exc_returns_trans,exc_returns)
        var_cov = np.divide(var_cov,exc_returns.shape[0])
        return var_cov

    #funkcja która liczy odchylenie standardowe w zależności od wag
    def get_portfolio_std_deviation(weights):
        portfolio_standard_deviation = np.sqrt(np.matmul(np.matmul(weights,variance_covariance_matrix(returns)), weights))
        return portfolio_standard_deviation     

    #funkcja która liczy oczekiwany zwrot portfolio w zależności od wag
    def get_portfolio_exp_return(weights):
        portfolio_exp_return = np.matmul(returns.mean(), weights)
        return portfolio_exp_return

    #funkcja która oblicza sharpe ratio portfolia w zależności od wag
    def get_portfolio_sharpe_ratio(weights):
        portfolio_sharpe_ratio = get_portfolio_exp_return(weights)/get_portfolio_std_deviation(weights)
        return portfolio_sharpe_ratio

    def get_portfolio_exp_return_reversed(weights):
        return 1/get_portfolio_exp_return(weights)

    

    def get_sharpe_ratio_reversed(weights):
        return 1/get_portfolio_sharpe_ratio(weights)


    
    comp_number = visdata.count()
    if comp_number > 0:
        max_expected_return = max(returns.mean())
        min_std_dev = min(returns.std())
        max_sharpe_ratio = max(sharpe_ratio['sharpe_ratio'])
        min_weight = min(wagi)
        print(min_weight)
        
        bnds = (0.05,1)
        bnds2 = []
        print('pierwotne wagi',wagi)

        for i in spolki:
            bnds2.append(bnds)
        
        bnds2 = tuple(bnds2)
        
        #OPTYMALIZACJA 1
        cons = ({'type': 'eq', 'fun': lambda x:  sum(x) - 1},
            {'type': 'ineq', 'fun': lambda x: min_std_dev - get_portfolio_std_deviation(x)})
        result = opt.minimize(get_portfolio_exp_return_reversed, wagi, bounds=bnds2, constraints=cons)
        print('wagi optymalizacja 1',result.x)

        #OPTYMALIZACJA 2
        cons2 = ({'type': 'eq', 'fun': lambda x:  sum(x) - 1},
            {'type': 'ineq', 'fun': lambda x: get_portfolio_exp_return(x) - max_expected_return})

        result2 = opt.minimize(get_portfolio_std_deviation, wagi, constraints=cons2,bounds=bnds2)
        
        print('wagi optymalizacja 2',result2.x)

        #OPTYMALIZACJA 3
        cons3 = ({'type': 'eq', 'fun': lambda x:  sum(x) - 1})
        

        result3 = opt.minimize(get_sharpe_ratio_reversed, wagi, bounds=bnds2, constraints=cons3)
        print('wagi optymalizacja 3',result3.x)



        #nowe_wagi*wartość_portfela=ile bedą warte te nowe
        new_values = result3.x*portfolio_value
        print(new_values)
        new_amount = new_values/portfolio['live price']
        print(new_amount)
        delta_amount = new_amount-portfolio['ilosc akcji']
        print(delta_amount)
        new_frame = {'new amount': new_amount, 'zmiana': delta_amount}
        new_portfolio = pd.DataFrame(new_frame)
        
        new_portfolio.loc[new_portfolio.zmiana > 0, 'akcja'] = "Dokup" 
        
        print(new_portfolio)
        #ile sztuk nowych akcji = te nowe/cena aktualna
        #stare_akcje-nowe_akcje = ile dokupic/sprzedać
    else:
        print('Portfolio jest puste')

    context = {'portfolio_current_state': portfolio_current_state, 'visdata': visdata, 'current_portfolio': current_portfolio,'delta_amount':delta_amount,'new_amount':new_amount}
    return render(request, 'optifolio/optimize.html', context)


@unauthenticated_user
def yahooPage(request):
    symbol = "GPW.WA"
    price = get_live_price(symbol)
    #table = get_data(symbol,start_date="06/05/2020",end_date="06/05/2021",index_as_date=False,interval="1d")
    #table = table[['close']]
    #html = table.to_html()
    context = {'symbol':symbol,'price':price}
    return render(request,'optifolio/yahoo.html', context)

@unauthenticated_user
def infoPage(request):
    context = {}
    return render(request, 'optifolio/infopage.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def og_infoPage(request):
    context = {}
    return render(request, 'optifolio/og_infopage.html',context)

@unauthenticated_user
def templatevisualisationPage(request):
    visdata = VisData.objects.all()
    context = {'visdata':visdata}
    return render(request, 'optifolio/templatevisualisationpage.html',context)


