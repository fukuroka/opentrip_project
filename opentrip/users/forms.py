from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomerRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Имя')
    last_name = forms.CharField(max_length=50, label='Фамилия')
    phone_number = forms.CharField(max_length=17, label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']



class HotelRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=17, label='Телефон')
    website = forms.CharField(max_length=100,label = 'Сайт')

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password1', 'password2']
