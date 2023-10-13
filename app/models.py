from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.query import QuerySet

class BankManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().order_by('balance')
    
    def order_by_name(self):
        return super().get_queryset().order_by('name')

class Bank(models.Model):
    name = models.CharField(max_length=30)
    balance = models.IntegerField()
    objects = models.Manager()
    banksorted = BankManager()    
    
    def __str__(self):
        return self.name

class PayPal(models.Model):
    name = models.CharField(max_length=30)
    balance = models.IntegerField()
    
    def __str__(self):
        return self.name

class Order(models.Model):    
    banks = models.ForeignKey(Bank, on_delete=models.CASCADE)
    paypals = models.ForeignKey(PayPal, on_delete=models.CASCADE)
    transfer = models.IntegerField()
    
