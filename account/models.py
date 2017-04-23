from django.db import models

# Create your models here.

class Account(models.Model):
  phone = models.CharField(max_length=100)
  gender = models.CharField(max_length=1)
#  language = models.ForeignKey(Language) # No Language setting per Registration nor Member. Detect from browser or device.

  profile_photo_url = models.CharField(max_length=100)

  phone = models.CharField(max_length=25)

  payment_method = models.CharField(max_length=10)
  payment_text = models.CharField(max_length=5)
  payment_token = models.CharField(max_length=70)

  dob = models.DateField()

  last_geo_lat = models.DecimalField(max_digits=9, decimal_places=6)
  last_geo_lng = models.DecimalField(max_digits=9, decimal_places=6)

  tos_accept_date = models.DateTimeField('Terms of Service Accept Date')
  tos_accept_version = models.CharField(max_length=15)

  last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

class AccountPartnerRoles(models.Model):
  account = models.ForeignKey(Account)
  role_name = models.CharField(max_length=25)
  role_description = models.CharField(max_length=50)
#  target_type = models.CharField(max_length=12)
#  target_id = models.ForeignKey('partner.')