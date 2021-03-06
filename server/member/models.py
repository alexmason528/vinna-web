import jwt
from django.db import models

from core.models import State, Country

from server.media.models import Image
from server.account.models import Account

from vinna.settings import BASE_URL

class Member(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    mailing_address_1 = models.CharField(max_length=40)
    mailing_address_2 = models.CharField(max_length=40, default='', blank=True)
    mailing_address_city = models.CharField(max_length=50)
    mailing_address_state = models.ForeignKey(State)
    mailing_address_zip = models.CharField(max_length=20)
    mailing_address_country = models.ForeignKey(Country)
    profile_image = models.ForeignKey(Image, null=True, blank=True)
    managed_account_token = models.CharField(max_length=50)

    security_hash = models.CharField(max_length=32, default='', blank=True)
    ssn_token = models.CharField(max_length=9, default='', blank=True)

    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.account.first_name +' '+self.account.last_name

    def get_payment_info(self):
        payment_info = MemberPaymentInfo.objects.get(member=self)
        return payment_info

class MemberPaymentInfo(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    text = models.CharField(max_length=15)
    token = models.CharField(max_length=70)
    routing_number = models.CharField(max_length=20)

    def __str__(self):
        return self.member.account.first_name+' '+self.member.account.last_name+' ('+self.type+', '+self.text+')'
