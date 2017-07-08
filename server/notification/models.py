from django.db import models

from server.business.models import Business
from server.account.models import Account
# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    state = models.BooleanField(default=0)
    link = models.CharField(max_length=150, blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    business = models.ForeignKey(Business)
    account = models.ForeignKey(Account, blank=True, null=True)

    def __str__(self):
    	return self.title
