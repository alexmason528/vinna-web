from django.contrib import admin
from .models import Account#, Role, AccountRole

# class AccountRoleListInline(admin.StackedInline):
#     model = AccountRole
#     extra = 1

# class AccountAdmin(admin.ModelAdmin):
#     inlines = (AccountRoleListInline,)

# class RoleAdmin(admin.ModelAdmin):
#     inlines = (AccountRoleListInline,)

# admin.site.register(Role)
admin.site.register(Account)#, AccountAdmin)