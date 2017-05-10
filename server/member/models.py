# Create your models here.
from django.db import models

class Member(models.Model):
#  language = models.ForeignKey(Language) # No Language setting per Registration nor Member. Detect from browser or device.
  account = models.ForeignKey('account.Account')

  mailing_address_1 = models.CharField(max_length=40)
  mailing_address_2 = models.CharField(max_length=40)
  mailing_address_city = models.CharField(max_length=50)
  mailing_address_state = models.ForeignKey('core.State')
  mailing_address_zip = models.CharField(max_length=20)
  mailing_address_country = models.ForeignKey('core.Country')

  security_hash = models.CharField(max_length=32)
  ssn_token = models.CharField(max_length=10)

  last_modified_date = models.DateTimeField('Last Modified', auto_now=True)
#  def __str__(self):
#    return self.name


class MemberPaymentInfo(models.Model):
  member = models.ForeignKey(Member)
  
  type = models.CharField(max_length=10) # bank, debit, mail
  text = models.CharField(max_length=5)
  token = models.CharField(max_length=70)
  