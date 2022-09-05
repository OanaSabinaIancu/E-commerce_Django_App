import re
from django.http import HttpResponse
from django.shortcuts import redirect

#Cream un decorator (o functie care are ca parametru o alta functie [de exemplu, daca declaram functia deasupra celei de login atunci aceasta va fi considerata a fi un parametru al functiei in cauza])

def unauthenticated_user(view_func):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_fun

#Cream un decorator care ne va indica ce utilizator face parte din fiecare tip de grup

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group =  request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                 return HttpResponse("Utilizator neautorizat")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exist():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('profile')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    
    return wrapper_function

