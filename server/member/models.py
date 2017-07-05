import jwt

from django.db import models

from core.models import State, Country

from server.media.models import Image
from server.account.models import Account

from vinna.settings import BASE_URL

class Member(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    mailing_address_1 = models.CharField(max_length=40)
    mailing_address_2 = models.CharField(max_length=40)
    mailing_address_city = models.CharField(max_length=50)
    mailing_address_state = models.ForeignKey(State)
    mailing_address_zip = models.CharField(max_length=20)
    mailing_address_country = models.ForeignKey(Country)
    profile_image = models.ForeignKey(Image, null=True, blank=True)
    managed_account_token = models.CharField(max_length=50)

    security_hash = models.CharField(max_length=32, null=True, blank=True)
    ssn_token = models.CharField(max_length=10, null=True, blank=True)

    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.account.first_name +' '+self.account.last_name

    def get_registration_link(self):
        return BASE_URL + 'client_member/download/?referral='+jwt.encode({'id': self.id}, 'secret').decode('utf-8')

class MemberPaymentInfo(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    type = models.CharField(max_length=10, default='bank') # bank, debit, mail
    text = models.CharField(max_length=4)
    token = models.CharField(max_length=70)
    routing_number = models.CharField(max_length=20)

    def __str__(self):
        return self.member.account.first_name+' '+self.member.account.last_name+' ('+self.type+', '+self.text+')'

class MemberReferral(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    friend_email_or_phone = models.CharField(max_length=40)
    friend_ip = models.CharField(max_length=15, null=True, blank=True)
    friend_user_agent = models.CharField(max_length=200, null=True, blank=True)
    friend_referrer = models.CharField(max_length=200, null=True, blank=True)
    connected = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now=True)
