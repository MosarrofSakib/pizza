from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

#this is to track the order not to determine the overall price (I think...)
class Pizza(models.Model):
    small = 'S'
    large = 'L'
    regular = 'Regular'
    sicilian = 'Sicilian'
    sizes = [(small, 'Small'), (large, 'Large')]
    types = [(regular, 'Regular'), (sicilian, 'Sicilian')]

    pizza_type = models.CharField(max_length=64, choices = types, default = regular)
    item = models.CharField(max_length=64)
    size = models.CharField(max_length=64, choices = sizes, default = small)
    toppings = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"


# class Regular(models.Model):
#     SMALL = 'S'
#     LARGE = 'L'
#
#     item = models.CharField(max_length=64)
#
#     PIZZA_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
#     pizza_size = models.CharField(max_length=64, choices = PIZZA_SIZE_CHOICES, default = SMALL)
#
#     num_toppings = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
#     price = models.DecimalField(max_digits = 4, decimal_places = 2)
#
#     def __str__(self):
#         return f"{self.item}, Toppings: {self.num_toppings}, Price: {self.price}"
#
# class Sicilian(models.Model):
#     SMALL = 'S'
#     LARGE = 'L'
#
#     item = models.CharField(max_length=64)
#
#     PIZZA_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
#     pizza_size = models.CharField(max_length=64, choices = PIZZA_SIZE_CHOICES, default = SMALL)
#
#     num_toppings = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
#     price = models.DecimalField(max_digits = 4, decimal_places = 2)
#
#     def __str__(self):
#         return f"{self.item} Toppings: {self.num_toppings} Price: {self.price}"

#idk how to handle the ones that have additional toppings; skipping for now
class Sub(models.Model):
    SMALL = 'S'
    LARGE = 'L'

    item = models.CharField(max_length=64)

    SUB_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
    sub_size = models.CharField(max_length=64, choices = SUB_SIZE_CHOICES, default = SMALL)

    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

class Dinnerplatter(models.Model):
    SMALL = 'S'
    LARGE = 'L'

    item = models.CharField(max_length=64)

    PLATTER_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
    platter_size = models.CharField(max_length=64, choices = PLATTER_SIZE_CHOICES, default = SMALL)

    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

class Pasta(models.Model):
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

class Salad(models.Model):
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

#consolidates items into one class model
class Cart(models.Model):
    #link the pizzas
    # regular = models.ForeignKey(Regular, on_delete=models.CASCADE)
    # sicilian = models.ForeignKey(Sicilian, on_delete=models.CASCADE)
    #pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)

#used to fulfill the order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Cart)
    complete = models.BooleanField(default = False)

# class Test(models.Model):
#     item = models.CharField(max_length=64)
#     price = models.DecimalField(max_digits = 4, decimal_places = 2)
#
#     def __str__(self):
#         return f"{self.item}"
