from django.contrib import admin

from .models import Member, MemberPaymentInfo

admin.site.register(Member)
admin.site.register(MemberPaymentInfo)
