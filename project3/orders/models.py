from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator

#this is to track the order not to determine the overall price (I think...)
class Toppings(models.Model):
    toppings = models.CharField(max_length=64)

class Regular(models.Model):
    SMALL = 'S'
    LARGE = 'L'

    item = models.CharField(max_length=64)

    PIZZA_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
    pizza_size = models.CharField(max_length=64, choices = PIZZA_SIZE_CHOICES, default = SMALL)

    num_toppings = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

class Sicilian(models.Model):
    SMALL = 'S'
    LARGE = 'L'

    item = models.CharField(max_length=64)

    PIZZA_SIZE_CHOICES = [(SMALL,'Small'), (LARGE, 'Large')]
    pizza_size = models.CharField(max_length=64, choices = PIZZA_SIZE_CHOICES, default = SMALL)

    num_toppings = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    price = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.item}"

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
