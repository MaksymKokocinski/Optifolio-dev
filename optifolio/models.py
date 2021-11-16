from django.db import models
#from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="user3.jpg",null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return self.name
		

class VisData(models.Model):
    BUY_SELL_CHOICES = [('+', 'Kupno'), ('-','Sprzedaz')]
    visdata_id = models.AutoField(primary_key=True,blank=True)
    user_name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL,blank=True)
    title = models.CharField(max_length=200, null=True,blank=True)
    buy_sell = models.CharField(max_length=8, choices=BUY_SELL_CHOICES, null=True, blank=True)
    date = models.DateField(auto_now_add=False,null=True,editable=True,blank=True)
    hour = models.TimeField(auto_now=False, auto_now_add=False,null=True,editable=True,blank=True)
    #nie wiem co tu jest nie tak, chcialam dodac ograniczenie wymagajace liczb dodatnich
    #shares_number = models.DecimalField(decimal_places=8,default=0,max_digits=999, null=True,blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    shares_number = models.DecimalField(decimal_places=8,default=0,max_digits=999, null=True,blank=True)
    course = models.DecimalField(decimal_places=2,default=0,max_digits=999,null=True,blank=True)
    fare = models.DecimalField(decimal_places=2,default=0,max_digits=999,null=True,blank=True)


    def __str__(self):
        return self.title if self.title else ''