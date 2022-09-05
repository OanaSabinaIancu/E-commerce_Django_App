from ast import Mod
from dataclasses import field, fields
from tkinter import Y
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Customer, Order, Product, ProductUser, RecoverEmail, ReviewProduct

#from .models import Comment

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        

class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Nume de utilizator'
            }
        )
    )

    firstName = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Prenume'
            }
        )
    )

    lastName = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Nume'
            }
        )
    )

    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Email'
            }
        )
    )
    
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Parola'
            }
        )
    )

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Confirma parola'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'firstName', 'lastName', 'email', 'password1', 'password2']

class CustomerForm(ModelForm):

    firstName = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Prenume'
            }
        )
    )

    lastName = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Nume'
            }
        )
    )

    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Email'
            }
        )
    )

    phone = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Email'
            }
        )
    )


    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class ProductUserForm(ModelForm):

    ingredients = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Lipeste reteta aici'
            }
        )
    )

    class Meta:
        model = ProductUser
        fields = '__all__'

class ProfileForm(ModelForm):

    firstName = forms.CharField(required=False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Prenume',
            }
        )
    )

    lastName = forms.CharField(required=False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Nume'
            }
        )
    )

    email = forms.CharField(required=False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Email'
            }
        )
    )

    phone = forms.CharField(required=False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Număr de telefon'
            }
        )
    )

    profile_pic = forms.ImageField(required=False,
       widget = forms.FileInput(
            attrs= {
                'class': 'block w-full text-sm text-purple-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none ',
                'placeholder': 'Caută imagine'
            }
        ) 
    )
    
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'email', 'profile_pic', 'phone']


class ReviewProductForm(ModelForm):

    revtitle = forms.CharField(required=True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Titlul recenziei'
            }
        )
    )

    revmess = forms.CharField(required=True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Mesajul recenziei'
            }
        )
    )

    class Meta:
        model = ReviewProduct
        fields = '__all__'
        exclude = ['rating', 'user']

class RecoverEmailForm(ModelForm):

    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder':'Email'
            }
        )
    )

    class Meta:
        model = RecoverEmail
        fields = '__all__'
        #exclude = ['rating', 'user']