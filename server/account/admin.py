from django.contrib import admin
from .models import Account, AccountPartnerRole, AccountPartnerRoleList

class AccountPartnerRoleListInline(admin.StackedInline):
    model = AccountPartnerRoleList
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountPartnerRoleListInline,)

class AccountPartnerRoleAdmin(admin.ModelAdmin):
    inlines = (AccountPartnerRoleListInline,)

admin.site.register(AccountPartnerRole)
admin.site.register(Account, AccountAdmin)