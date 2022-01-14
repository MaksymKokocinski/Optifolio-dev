from django.db import models
#from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from yahoo_fin.stock_info import tickers_sp500

class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="user3.jpg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return self.name
		
class TicName(models.Model):
    tic_sym = models.CharField(primary_key=True,max_length=10,null=False,blank=True)
    tic_name = models.CharField(max_length=100,null=False,blank=True)

    def __str__(self) :
        return self.tic_name 

class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True,blank=True)
    portfolio_title = models.CharField(unique=True,max_length=200, null=True,blank=True)
    user_name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL,blank=True)
    
    p_shares_num_sum = models.DecimalField(decimal_places=2,default=0,max_digits=999,editable=True, null=True,blank=True)
    p_last_mod_date = models.DateField(auto_now_add=False,null=True,editable=True,blank=True)
    p_comp_num_sum = models.DecimalField(decimal_places=2,default=0,max_digits=999,editable=True, null=True,blank=True)
    p_to_buy_percentage = models.CharField(max_length=200,editable=True, null=True,blank=True)
    p_profit_earned = models.DecimalField(decimal_places=6,editable=True,default=0,max_digits=999, null=True,blank=True)
    
    def __str__(self):
        return self.portfolio_title if self.portfolio_title else ''


class VisData(models.Model):
    list_names = []
    for i in tickers_sp500():
        list_names.append((i,i))
    BUY_SELL_CHOICES = [('+', 'Kupno'), ('-','Sprzedaz')]
    visdata_id = models.AutoField(primary_key=True,blank=True)
    user_name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL,blank=True)

    TITLE_CHOICES = list_names
    title = models.CharField(max_length=15, null=True,blank=True)
    title2 = models.CharField(max_length=200, choices = TITLE_CHOICES, null=True,blank=False)

    portfolio_name = models.ForeignKey(Portfolio,on_delete=models.SET_NULL,blank=True, null=True)

    buy_sell = models.CharField(max_length=8, choices=BUY_SELL_CHOICES, null=True, blank=True)
    date = models.DateField(auto_now_add=False,null=True,editable=True,blank=True)
    hour = models.TimeField(auto_now=False, auto_now_add=False,null=True,editable=True,blank=True)
    shares_number = models.DecimalField(decimal_places=8,default=0,max_digits=999, null=True,blank=True)
    course = models.DecimalField(decimal_places=2,default=0,max_digits=999,null=True,blank=True)
    fare = models.DecimalField(decimal_places=2,default=0,max_digits=999,null=True,blank=True)
    
    def __str__(self):
        return self.title if self.title else ''
