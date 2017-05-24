from django.db import models

from server.member.models import Member
from server.business.models import Business
# Create your models here.

class Review(models.Model):
    member = models.ForeignKey(Member)
    business = models.ForeignKey(Business)
    rating = models.IntegerField()
    review = models.CharField(max_length = 100, null = True, blank = True)

    class Meta:
        unique_together = ('member', 'business')
