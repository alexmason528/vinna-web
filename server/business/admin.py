from django.contrib import admin

from .models import Business, BusinessBillingInfo, Category, SubCategory

admin.site.register(Business)
admin.site.register(BusinessBillingInfo)
admin.site.register(Category)
admin.site.register(SubCategory)
