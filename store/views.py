from datetime import datetime
from email import message
import email
from re import template
from debugpy import configure
from django.dispatch import receiver
from matplotlib.style import use
from numpy import product
from requests import request
from store.decorators import unauthenticated_user
from store.models import Product
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json

#importam formularul din django

from django.contrib.auth.forms import UserCreationForm

#importam functia care apelaza cookies pentru checkout


#importam o functie pentru a face codul mai bine organizat

from .utils import cartData

#Cream views pentru login/ register

from .forms import OrderForm, CreateUserForm, ProductUserForm

#One time message pentru validarea unui cont nou

from django.contrib import messages

#Avem nevoie pentru a realiza operatiile de login si register

from django.contrib.auth import authenticate, login, logout

#Importam decoratorii

from .decorators import unauthenticated_user, allowed_users, admin_only

#Adaugam utilizatorul la un grup (admin/customer)

from django.contrib.auth.models import Group

#Adaugam functiile de filtrare

from .filters import ProductFilter

from .forms import *

#Importam librarie pentru trimiterea email-urilor

from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

def store(request):
    
    #Se extrag datele din cos printr-o cerere catre server

    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    #Se extrag toate obiectele din tabelul cu produse

    products = Product.objects.all()

    #Se calculeaza toate reducerile
    
    context = {'products' : products, 'cartProd' : cartProd, 'shipping' : False}
    
    return render(request, 'store/store.html', context)

def cart(request):

    cartdata = cartData(request)
    cartProd = cartdata['cartProd']
    order = cartdata['order']
    items = cartdata['items']

    for item in items:
        item.product.price = item.product.price - item.product.price * item.product.sales/100

    context = { 'items' : items, 'order' : order, 'cartProd' : cartProd, 'shipping' : False}
    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartProd = data['cartProd']

    for item in items:
        item.product.price = item.product.price - item.product.price * item.product.sales/100

    context = {'titlu':"Plata se face aici", 'order':order, 'items':items, 'cartProd':cartProd, 'shipping' : False}
    return render(request, 'store/checkout.html', context)


def procOrderPayment(request):
    status = 'in asteptare'
    transaction_id = datetime.now().timestamp()
    dataOrder = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
    
    total = float(dataOrder['form']['total'])
    order.transaction = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        order.status = status
    order.save()

    return JsonResponse('Plata efectuata', safe = False)

def successMsg(request, args):
    amount = args
    return render(request, '/success.html', {'amount':amount})

#@allowed_users(allowed_roles= ['admin'])

def updateItem(request):
    data = json.loads(request.body)
    
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = productId)

    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

   #verificam ce tip de operatie a fost ceruta
    

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    #retinem noua valoare a cantitatii din articol

    orderItem.save()

    #verificam daca mai sunt comandate produse de un anumit tip sau nu

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Articolul a fost adaugat in cos", safe=False)

#@allowed_users(allowed_roles= ['admin'])

def description(request):
        data = cartData(request)
        cartProd = data['cartProd']

        products = Product.objects.all()

        myFilter =  ProductFilter(request.GET, queryset = products)

        products = myFilter.qs

        context = {'titlu':"Ceva", 'products' : products, 'cartProd' : cartProd, 'shipping' : False, 'myFilter': myFilter}
        
        return render(request, 'store/description.html', context)

@unauthenticated_user
#@allowed_users(allowed_roles= ['admin'])        

def loginPage(request):
        cartdata = cartData(request)

        cartProd = cartdata['cartProd']

        #Cream form-ul pentru autentificare

        form = CreateUserForm()

        #Extragem datele scrise in forma si le adaugam la back-end

        if request.method =="POST":

            #Extragem datele din casuta de login

            username = request.POST.get('username')
            password = request.POST.get('password')

            #Verificam daca datele sunt in baza de date

            user = authenticate(request, username = username, password = password)

            #Daca utilizatorul e in baza de date, dar nu e logat niciun cont, ii facem login

            if user is not None:
                login(request, user)

                #Cream customer

                return redirect('store')
            else:
                messages.info(request, 'Campul cu nume de utilizator sau cel cu parola lipseste sau este trecut incorect')

        context = {'cartProd' : cartProd, 'form':form}
        return render(request, 'store/login.html', context)

@unauthenticated_user

def reqPassword(request):
    cartdata = cartData(request)

    cartProd = cartdata['cartProd']

    #Cream form-ul necesar realizarii unei cereri pentru generarea unei noi parole

    form = RecoverEmailForm()

    if request.method == 'POST':
        form = RecoverEmailForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Email-ul a fost introdus în baza de date, te rugăm să aştepţi ca un administrator să îţi genereze o altă parolă')
            return redirect('store')

    context = {'cartProd' : cartProd, 'form': form}
    return render(request, 'store/reqPassword.html', context)


@unauthenticated_user
#@allowed_users(allowed_roles= ['admin'])

def register(request):

    cartdata = cartData(request)

    cartProd = cartdata['cartProd']

    #Cream form-ul pentru autentificare
    form = CreateUserForm()

    #Extragem datele scrise in forma si le adaugam la back-end

    if request.method =="POST":
        form = CreateUserForm(request.POST)
        #form = UserCreationForm(request.POST)
        
        #Validam datele introduse in form si le salvam

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')

            customer = Customer.objects.create(
                user = user,
                username = request.POST.get("username"),
                firstName = request.POST.get("firstName"),
                lastName = request.POST.get("lastName"),
                email = request.POST.get("email"),
            )

            customer.save()

            messages.success(request, 'Contul a fost creat cu succes pentru '+ username)

            return redirect('loginPage')

    context = {'cartProd' : cartProd, 'form':form}
    return render(request, 'store/register.html', context)

#@allowed_users(allowed_roles= ['admin'])

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

#@allowed_users(allowed_roles= ['customer'])

def profile(request):
    cartdata = cartData(request)

    cartProd = cartdata['cartProd']

    custom = request.user.customer

    customer = custom

    ord = Order.objects.all().filter(customer=custom)

    orders = Order.objects.all().filter(customer=custom).first()
    orderItem = OrderItem.objects.all().filter(order=orders)

    context = {'cartProd' : cartProd, 'customer': customer, 'orderItem':orderItem, 'orders':orders, 'ord':ord}
    return render(request, 'store/profile.html', context)


def updateProfile(request):
    cartdata = cartData(request)

    cartProd = cartdata['cartProd']

    custom = request.user.customer

    form = ProfileForm()

    form.fields['firstName'].widget.attrs['value'] = custom.firstName
    form.fields['lastName'].widget.attrs['value'] = custom.lastName
    form.fields['email'].widget.attrs['value'] = custom.email
    form.fields['phone'].widget.attrs['value'] = custom.phone

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            #form.save()
            custom.firstName = form.cleaned_data['firstName']
            custom.lastName = form.cleaned_data['lastName']
            custom.email = form.cleaned_data['email']
            custom.phone = form.cleaned_data['phone']
            custom.profile_pic.delete(save = False)

            if 'profile_pic' in request.FILES:
                custom.profile_pic = request.FILES['profile_pic']
            custom.save()
            return redirect('profile')

        

    context = {'cartProd' : cartProd, 'custom': custom, 'form':form}
    return render(request, 'store/updateProfile.html', context)


#@allowed_users(allowed_roles= ['customer'])

def product(request, id):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    product = Product.objects.filter(id = id).first()

    review = ReviewProduct.objects.all()

    reviews = ReviewProduct.objects.all().filter(reviewProd=product.id)

    ingred = product.ingredients.split(",")

    alerg = product.alergens.split(",")

    discount = product.price - (product.sales*product.price/100)

    form = ReviewProductForm()

    form.fields['reviewProd'].widget.attrs['value'] = product

    if request.method == 'POST':
        form = ReviewProductForm(request.POST)

        if form.is_valid():

            data = ReviewProduct()

            data.revtitle = form.cleaned_data['revtitle']
            data.revmess = form.cleaned_data['revmess']
            data.reviewProd = product

            messages.success(request, 'Îţi mulţumim pentru comentariu! Ne bucurăm că ne ajuţi să ne dezvoltăm afacerea şi vă mulţumim că ne sunteţi alături!')
            data.save()


    context = { 'product':product, 'cartProd' : cartProd, 'ingred': ingred, 'alerg' : alerg, 'discount': discount, 'form' : form, 'reviews': reviews }
    
    return render(request, 'store/product.html', context)

#@allowed_users(allowed_roles= ['admin'])

def special(request):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    form = ProductUserForm()

    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('store')

    for product in products:
        if product.category == 'special':
            prod = product
            break

    context = { 'prod' : prod, 'cartProd' : cartProd, 'form': form }
    
    return render(request, 'store/special.html', context)

#@allowed_users(allowed_roles= ['admin'])

def recipes(request):

    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    recipes = Recipe.objects.all()

    nrrec = Recipe.objects.all().count()
    nrlist = []
    for i in range(nrrec):
        nrlist.append(i)

    context = { 'recipes' : recipes, 'cartProd' : cartProd, "nrrec":nrrec}
    return render(request, 'store/recipes.html', context)

#@allowed_users(allowed_roles= ['admin'])

def recipe(request, id):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    recipe = Recipe.objects.filter(id = id).first()

    cakeing = recipe.cakeIng.split(",")
    creaming = recipe.creamIng.split(",")

    context = { 'recipe':recipe, 'cartProd' : cartProd, 'cakeing':cakeing, 'creaming':creaming }
    
    return render(request, 'store/recipe.html', context)

def presentation(request):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    
    context = { 'cartProd' : cartProd }
    
    return render(request, 'store/presentation.html', context)

def eroare(request, exception):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']

    context = { 'cartProd' : cartProd }

    return render(request, 'store/404.html', context)

def error403(request):
    cartdata = cartData(request)
    cartProd = cartdata['cartProd']


    context = { 'cartProd' : cartProd }

    return render(request, 'error403.html', context) 

