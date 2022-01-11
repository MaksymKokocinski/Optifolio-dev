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
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id = pk)

    context = {'customer':customer,}
    return render(request, 'optifolio/customer.html',context)

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
def addVisData(request):
    current_user_name = request.user.customer

    form = AddSharesForm(request.POST or None)
    if request.method == 'POST':
        print(form.data)
        if form.is_valid():
            print(form.cleaned_data)
            publish = form.save(commit=False)
            publish.user_name = current_user_name #Adding username to form
            publish.save()
            return redirect('visualisationpage')
    else:
            form = AddSharesForm()


    context = {'form': form, 'current_user_name':current_user_name}
    return render(request, 'optifolio/add_transaction.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateVisData(request, vispk):
    transaction = VisData.objects.get(visdata_id=vispk)
    form = AddSharesForm(instance=transaction)

    if request.method == 'POST':
        form = AddSharesForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('visualisationpage')

    context = {'form': form}
    return render(request, 'optifolio/update_transaction.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteVisData(request, vispk):
    transaction = VisData.objects.get(visdata_id=vispk)
    if request.method == "POST":
        transaction.delete()
        return redirect('visualisationpage')
    context = {'item': transaction}
    return render(request, 'optifolio/delete_transaction.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def summaryPage(request):
    current_user_name = request.user.customer
    visdata = request.user.customer.visdata_set.all()
    all_user_portfolio = request.user.customer.portfolio_set.all()

    count_portfolio = all_user_portfolio.count()
    if count_portfolio > 0:
        #print('test2',count_portfolio,all_user_portfolio)
        for temp in range (count_portfolio):
            print(all_user_portfolio[temp])

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



    print('visdata',visdata)

    print('smth')

    print('portfolio',all_user_portfolio)

    comp_number = visdata.count()
    if comp_number > 0:
        
        shares_num = visdata.aggregate(Sum(('shares_number')))
        shares_num_sum = (shares_num['shares_number__sum'])
        shares_num_sum = format(shares_num_sum, ".0f")
        #profit_earned = visdata.aggregate(Sum(('course')))
        #profit_sum = (profit_earned['course__sum'])
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
        
        #for customer restriction delete object and change VisData to visdata
        aggregated_data = visdata.annotate(
        intermid_result=F('course') - F('fare') 
        ).annotate(
        record_total=F('shares_number') * F('intermid_result')
        ).aggregate(
        total=Sum('record_total')
        )
        profit_earned = aggregated_data['total']
        profit_earned = format(profit_earned, ".2f")
        print('changes',shares_num_sum,fare_sum,mod_date,to_buy,to_sell,to_buy_percentage,profit_earned)

    else:
        shares_num_sum = 0
        fare_sum = 0
        mod_date = 'brak'
        to_buy = 0
        to_sell = 0
        to_buy_percentage = 0
        profit_earned = 0
    
    context = {'form':form,'comp_number': comp_number, 'shares_num':shares_num_sum,'to_buy_percentage':to_buy_percentage, 'all_user_portfolio':all_user_portfolio,
     'profit_earned': profit_earned, 'fare_sum':fare_sum,'mod_date':mod_date,'current_user_name':current_user_name}
    return render(request, 'optifolio/summary.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def visPage(request, pk):
    current_user_name = request.user.customer
    current_portfolio = Portfolio.objects.get(portfolio_id = pk)
    visdata = current_portfolio.visdata_set.all()

    form = AddSharesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            publish = form.save(commit=False)
            publish.user_name = current_user_name #Adding username to form
            publish.save()
            return redirect('visualisationpage')
    else:
            form = AddSharesForm()

     
    context = {'current_portfolio':current_portfolio, 'visdata':visdata,'current_user_name':current_user_name,}
    return render(request, 'optifolio/vispage.html', context)

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

@unauthenticated_user
def templatevisualisationPage(request):
    visdata = VisData.objects.all()
    context = {'visdata':visdata}
    return render(request, 'optifolio/templatevisualisationpage.html',context)


