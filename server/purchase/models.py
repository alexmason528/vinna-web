from django.utils import timezone

from django.db import models
from server.business.models import Business
from server.member.models import Member
from server.account.models import Account

class Purchase(models.Model):
  
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    # description = models.CharField(max_length=500, null=True, blank=True)
    business = models.ForeignKey(Business)
    cashier_account = models.ForeignKey(Account)
    post_date = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)

    account = models.ForeignKey(Account, related_name="purchase_member")
    member_referral = models.ForeignKey(Member, related_name="purchase_member_referral", default='', blank=True)

    posted = models.BooleanField(default=0)

    business_percent = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    business_amount = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    business_amount_processed = models.BooleanField(default=0, blank=True)
    business_amount_processed_date = models.DateTimeField('Business Amount Processed Date', default=timezone.now, blank=True)

    member_percent = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    member_amount = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    member_amount_processed = models.BooleanField(default=0, blank=True)
    member_amount_processed_date = models.DateTimeField('Member Amount Processed Date', default=timezone.now, blank=True)

    member_ref_percent = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    member_ref_amount = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True)
    member_ref_amount_processed = models.BooleanField(default=0, blank=True)
    member_ref_amount_processed_date = models.DateTimeField('Member Referral Amount Processed Date', default=timezone.now, blank=True)

    void_date = models.DateTimeField(default=timezone.now, verbose_name='Void Date')
