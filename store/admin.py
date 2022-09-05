from django.contrib import admin

# Importam toate entitatile create in models

from .models import *
# Inregistreaza-ti modelul aici

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)
admin.site.register(Recipe)
admin.site.register(ProductUser)
admin.site.register(ReviewProduct)
admin.site.register(RecoverEmail)
