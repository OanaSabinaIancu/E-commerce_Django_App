from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings

from django.conf.urls.static import static

#importam views predefinite pentru autentificare

from django.contrib.auth import views as auth_views

#importuri pentru 404 si 403

from django.shortcuts import render

urlpatterns = [
    path('', views.store, name="store"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('processOrder/', views.procOrderPayment, name= "processOrder"),
    path('update_item/', views.updateItem, name="update_item"),
    path('description/', views.description, name="description"),

    path('loginPage/', views.loginPage, name="loginPage"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name= "register"),

    path('recipes/', views.recipes, name= "recipes"),
    path('special/', views.special, name= "special"),

    path('/<str:id>', views.product, name= "product"),

    path('store/<str:id>', views.product, name= "product"),
    path('store/product/<str:id>', views.product, name= "product"),
    path('description/product/<str:id>', views.product, name= "product"),
    path('description/<str:id>', views.product, name= "product"),

    path('recipes/<str:id>', views.recipe, name= "recipe"),
    path('profile/', views.profile, name= "profile"),
    

    path('presentation/', views.presentation, name= "presentation"),

    #preluam views pentru resetarea parolei
    #path('reqPssword/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reqPssword/', views.reqPassword, name="reset_password"),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    #uidb = parola in baza 64
    #token => verifica daca parola e valida

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = "password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name = "password_reset_complete"),

    path('updateProfile/', views.updateProfile, name="updateProfile")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)