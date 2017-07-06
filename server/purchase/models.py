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
    balance = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)

    member = models.ForeignKey(Member, related_name="purchase_member")
    member_referral = models.ForeignKey(Member, related_name="purchase_member_referral", null=True, blank=True)

    posted = models.BooleanField(default=0)

    business_percent = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    business_amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    business_amount_processed = models.BooleanField(default=0, blank=True)
    business_amount_processed_date = models.DateTimeField('Business Amount Processed Date', null=True, blank=True)

    member_percent = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    member_amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    member_amount_processed = models.BooleanField(default=0, blank=True)
    member_amount_processed_date = models.DateTimeField('Member Amount Processed Date', null=True, blank=True)

    member_ref_percent = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    member_ref_amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    member_ref_amount_processed = models.BooleanField(default=0, blank=True)
    member_ref_amount_processed_date = models.DateTimeField('Member Referral Amount Processed Date', null=True, blank=True)

    void_date = models.DateTimeField(auto_now=True, verbose_name='Void Date')
