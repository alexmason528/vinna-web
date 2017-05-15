from django.contrib import admin
from .models import Customer, CreditCard, BankAccount
# Register your models here.
admin.site.register(Customer)
admin.site.register(CreditCard)
admin.site.register(BankAccount)