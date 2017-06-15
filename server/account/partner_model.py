from django.db import models
from django.conf import settings

from core.models import Language
from server.account.models import Account
from server.business.models import Business

class AccountPartnerRole(models.Model):
    account = models.ForeignKey(Account)
    business = models.ForeignKey(Business)
    role = models.CharField(max_length=10)
    description = models.CharField(max_length=100, null=True, blank=True)