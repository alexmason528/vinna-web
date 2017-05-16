from django.contrib import admin
from .models import Account, AccountPartnerRole

class AccountPartnerRoleListInline(admin.StackedInline):
    model = Account.partner_roles.through

class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountPartnerRoleListInline,)
    exclude = ('partner_roles',)

class AccountPartnerRoleAdmin(admin.ModelAdmin):
    inlines = (AccountPartnerRoleListInline,)

admin.site.register(AccountPartnerRole)
admin.site.register(Account, AccountAdmin)