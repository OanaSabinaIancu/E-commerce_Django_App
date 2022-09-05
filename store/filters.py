import django_filters
from django.forms.widgets import Input, NumberInput

from decimal import Decimal

from matplotlib import widgets

from .models import *

class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter( 
        lookup_expr = "icontains", 
        widget = Input(
            attrs = {
                'class': 'form-control relative flex-auto min-w-0 block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', 'placeholder': 'Sortare după nume'
            }
        )
    )

    price = django_filters.CharFilter(
        lookup_expr= "lte"
    )

    class Meta:
        model = Product
        
        fields = [ 'name','alergens', 'sales', 'vegan', 'category']
        exclude = ['price']