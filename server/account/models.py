from django.db import models
from django.conf import settings
from core.models import Language

class Role(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    dob = models.DateField()
    gender = models.CharField(choices=((u'F',u'Female'),(u'M',u'Male')), max_length=1)
    profile_photo_url = models.ImageField(upload_to='images/', null=True, blank=True)
    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)
    roles = models.ManyToManyField(Role, through='AccountRole')

    def __str__(self):
        return self.first_name+' '+self.last_name

class AccountRole(models.Model):
    account = models.ForeignKey(Account)
    role = models.ForeignKey(Role)

    class Meta:
        unique_together = ('account', 'role',)