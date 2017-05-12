from django.db import models
from django.conf import settings

# Create your models here.

# Account. Holds Base account information for Employees
#    and for adding support for businesses to support multiple accounts in the future.
class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey('core.Language')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    dob = models.DateField()
    gender = models.CharField(choices=((u'F',u'Female'),(u'M',u'Male')), max_length=1)
    profile_photo_url = models.CharField(max_length=100, null=True, blank=True)
    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

#    language = models.ForeignKey(Language) # No Language setting per Registration nor Member. Detect from browser or device.
#    email = models.CharField(max_length=75)
#    payment_method = models.CharField(max_length=10)
#    payment_text = models.CharField(max_length=5)
#    payment_token = models.CharField(max_length=70)
#    last_geo_lat = models.DecimalField(max_digits=9, decimal_places=6)
#    last_geo_lng = models.DecimalField(max_digits=9, decimal_places=6)
#    tos_accept_date = models.DateTimeField('Terms of Service Accept Date')
#    tos_accept_version = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name+' '+self.last_name
        

class AccountPartnerRole(models.Model):
    account = models.ForeignKey(Account, related_name = 'accountpartnerroles', on_delete=models.CASCADE)
    role_name = models.CharField(max_length=25)
    role_description = models.CharField(max_length=50)

    #  target_type = models.CharField(max_length=12)
    #  target_id = models.ForeignKey('partner.')
    def __str__(self):
        return self.account.first_name+' '+self.account.last_name+' ('+self.role_name+')'