# Create your models here.
from django.db import models
from server.media.models import Image

class Member(models.Model):
    account = models.OneToOneField('account.Account', on_delete=models.CASCADE)

    mailing_address_1 = models.CharField(max_length=40)
    mailing_address_2 = models.CharField(max_length=40)
    mailing_address_city = models.CharField(max_length=50)
    mailing_address_state = models.ForeignKey('core.State')
    mailing_address_zip = models.CharField(max_length=20)
    mailing_address_country = models.ForeignKey('core.Country')
    profile_image = models.OneToOneField(Image, null=True, blank=True)

    security_hash = models.CharField(max_length=32)
    ssn_token = models.CharField(max_length=10)

    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.account.first_name +' '+self.account.last_name


class MemberPaymentInfo(models.Model):
    member = models.ForeignKey(Member)

    type = models.CharField(max_length=10) # bank, debit, mail
    text = models.CharField(max_length=5)
    token = models.CharField(max_length=70)

    def __str__(self):
        return self.member.account.first_name+' '+self.member.account.last_name+' ('+self.type+', '+self.text+')'
