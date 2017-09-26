from django.db import models

from server.account.models import Account
from server.business.models import Business
# Create your models here.

class Review(models.Model):
  account = models.ForeignKey(Account)
  business = models.ForeignKey(Business)
  rating = models.IntegerField()
  review = models.FloatField(max_length = 100, null = True, blank = True)
  approved = models.BooleanField(default=0)
  approved_date = models.DateTimeField(null=True, blank=True)

  class Meta:
    unique_together = ('account', 'business')
