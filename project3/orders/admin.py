from django.contrib import admin
from .models import Regular, Sicilian, Sub, Dinnerplatter, Pasta, Salad, Toppings

# Register your models here.

admin.site.register(Regular)
admin.site.register(Sicilian)
admin.site.register(Sub)
admin.site.register(Dinnerplatter)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Toppings)
