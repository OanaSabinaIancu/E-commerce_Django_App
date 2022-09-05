from django.db import models

from django.contrib.auth.models import User
from django.forms import ImageField
from django.utils import tree
from numpy import true_divide

from datetime import datetime 


# Cream o clasa pentru cumparator

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    username = models.CharField(max_length=301, null=True)
    firstName = models.CharField(max_length=301, null=True)
    lastName = models.CharField(max_length=301, null=True)
    email = models.CharField(max_length=301, null=True)

    profile_pic = models.ImageField(default='C:/Users/iancu/Desktop/prajituria/static/images/profil3.jpg', blank = True)
    phone = models.CharField(max_length=50, null = True)

    #note = models.CharField(max_length=99999999999999999999, null=True)

    def __str__(self):
        return str(self.firstName)+" "+str(self.lastName)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return '/static' + url

    @property
    def profileURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return '/static' + url


# Cream o clasa pentru produse

class Product(models.Model):


    name = models.CharField(max_length=301, null=True)
    price = models.DecimalField(max_digits= 5, decimal_places= 2 )

    ingredients = models.CharField(max_length=5000, null = True)
    

    sales = models.IntegerField(blank=True, null=True)

    #Se dorea a fi folosita si pentru rezervari in magayin, dar mai vedem

    digital = models.BooleanField(default=False, null=True, blank=False)

    # Folosim variabila *vegan* pentru a retine daca produsul este vegan sau nu

    vegan = models.BooleanField(default=False, null=True, blank=False)


    #Selectam categoriile din care pot face parte produsele

    categ = (
        ( 'torturi', 'torturi' ),
        ( 'briose', 'briose'),
        ('clatite', 'clatite'),
        ('pandispan', 'pandispan'),
        ('prajitura', 'prajitura'),
        ('biscuiti', 'biscuiti'),
        ('special', 'special'),

    )

    category =  models.CharField(max_length=500, null = True, choices= categ)

    #Selectam tipurile de alergeni 

    alerg = (
        ('lactoza', 'lactoza'),
        ('gluten', 'gluten'),
        ('fără alergeni', 'fără alergeni')
    )

    alergens = models.CharField(max_length=500, null = True, choices= alerg)

    image = models.ImageField(null = True, blank = True)


    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return '/static' + url

class ReviewProduct(models.Model):

    reviewProd = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True, blank = True)

    revtitle = models.CharField(max_length=300, null = True)

    revmess = models.CharField(max_length=500, null = True)

    rating = models.DecimalField(max_digits= 2, decimal_places= 2, default= 0.0 )

    published = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.revtitle

class ProductUser(models.Model):
  ingredients = models.CharField(max_length=5000, null = True) 

  def __str__(self):
        return self.ingredients 

# Cream o clasa de comenzi, aceasta va avea nevoie de o relatia 1-M intre Comanda si Utilizator

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null = True)

    Status = (
        ('in asteptare', 'in asteptare'),
        ('livrat', 'livrat')
    )

    status = models.CharField(max_length=100, null = True, choices=Status, default='in asteptare')

    @property
    def shipping(self):
        shipping = False #momentan produsele pot fi ridicate doar din magazin
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__ (self):
        return str(self.id)

# Cream articolele ce urmeaza a fi cuparate

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True)
    quantity = models.IntegerField(default=0, null= True, blank= True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__ (self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price*self.quantity
        return total

# Cream o clasa pentru a determina adresa de livrare a produselor

class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True, blank = True)
    address = models.CharField(max_length=301, null=True)
    city = models.CharField(max_length=301, null=True)
    state = models.CharField(max_length=301, null=True)
    zipcode = models.CharField(max_length=301, null=True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__ (self):
        return self.address
    
class Recipe(models.Model):
    title = models.CharField(max_length=500, null = True)
    cakeIng = models.CharField(max_length= 5000, null = True)
    creamIng = models.CharField(max_length= 5000, null = True)
    cakePrep = models.CharField(max_length= 5000, null = True)
    creamPrep = models.CharField(max_length= 5000, null = True)
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = str(self.image.url)
        except:
            url = ''
        return '/static' + url

class RecoverEmail(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True)
    email = models.CharField(max_length=500, null = True)

    def __str__(self):
        return self.email