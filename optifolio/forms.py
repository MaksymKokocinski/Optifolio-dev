from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django import forms

from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class VisForm(ModelForm):
    class Meta:
        model = VisData
        fields = '__all__'
        exclude = ['user_name']

#class AddPortfolioForm(ModelForm):
 #   class Meta:
  #      model = Portfolio
   #     fields = '__all__'

class AddSharesForm(ModelForm):
    class Meta:
        model = VisData
        fields = '__all__'

    def clean_shares_number(self):
        data = self.cleaned_data.get('shares_number')
        if data:
            if  data <= 0:
                raise forms.ValidationError('Enter a positive value')
            return data

    def clean_course(self):
        data = self.cleaned_data.get('course')
        if data:
            if  data <= 0:
                raise forms.ValidationError('Enter a positive value')
            return data

    def clean_fare(self):
        data = self.cleaned_data.get('fare')
        if data:
            if  data < 0:
                raise forms.ValidationError('Enter a non-negative value')
            return data










