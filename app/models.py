from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    supplier_name = models.CharField(max_length=200)
    date = models.DateField()
    invoice_number = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def sub_total(self):
        return self.quantity * self.rate

    @property
    def tax_amount(self):
        return (self.sub_total * self.product.tax_percentage) / 100

    @property
    def grand_total(self):
        return self.sub_total + self.tax_amount