from django.forms import ModelForm
from django.forms import DateInput, TimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django import forms

from .models import *
from django.utils.timezone import now

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

class AddPortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'
        exclude = ['user_name']

class AddSharesForm(ModelForm):
    class Meta:
        model = VisData
        fields = '__all__'
        widgets = {
            'date': DateInput,
            'hour': TimeInput
        }

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
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            if cleaned_data['date'] and  cleaned_data['hour']:
                date_value = cleaned_data.get('date')
                hour_value = cleaned_data.get('hour')
                if date_value > now().date():
                    raise forms.ValidationError("You can't enter a future date")
                elif date_value == now().date() and hour_value > now().time():
                    raise forms.ValidationError("You can't enter a future hour")
            return cleaned_data








