from django.forms import ModelForm, SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms


from django.forms import DateInput

class UserAddBookingForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['destination', 'airline', 'hotel', 'arrival_date', 'departure_date']
        widgets = {
            'arrival_date': DateInput(attrs={'type': 'date'}),
            'departure_date': DateInput(attrs={'type': 'date'}),
        }
    exclude = ['user']

class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
        widgets = {
            'arrival_date': SelectDateWidget(),
            'departure_date': SelectDateWidget()
        }
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','phone','username', 'email', 'password1', 'password2']  # Added password1 and password2 for password confirmation
    