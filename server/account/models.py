from django.db import models
from django.conf import settings
from core.models import Language

class AccountPartnerRole(models.Model):
    role_name = models.CharField(max_length=25)
    role_description = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name
 
class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    dob = models.DateField()
    gender = models.CharField(choices=((u'F',u'Female'),(u'M',u'Male')), max_length=1)
    profile_photo_url = models.CharField(max_length=100, null=True, blank=True)
    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)
    partner_roles = models.ManyToManyField(AccountPartnerRole, through='AccountPartnerRoleList')

    def __str__(self):
        return self.first_name+' '+self.last_name

class AccountPartnerRoleList(models.Model):
    account = models.ForeignKey(Account)
    partner_role = models.ForeignKey(AccountPartnerRole)
