from django.db import models

from server.account.models import Account
from .models import Business

class Invitation(models.Model):
    business = models.ForeignKey(Business)
    email = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
