from django.contrib import admin
from .models import Pizza, Sub, Dinnerplatter, Pasta, Salad, Cart, Order, Sicilian

# Register your models here.

# admin.site.register(Regular)
admin.site.register(Sicilian)
admin.site.register(Pizza)
admin.site.register(Sub)
admin.site.register(Dinnerplatter)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Cart)
admin.site.register(Order)
