from django.db import models

from core.models import Country, State
from server.account.models import Account
from server.media.models import BusinessImage

def upload_profile_image_to(instance, filename):
    import os
    from django.utils.timezone import now

    filename_base, filename_ext = os.path.splitext(filename)
    return 'profile/%s/%s%s' % (
        now().strftime("%Y%m%d"),
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )

class SubCategory(models.Model):
    category = models.ForeignKey('business.Category')
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Category(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

    def get_sub_categories(self):
        sub_categories = SubCategory.objects.filter(category = self)
        return sub_categories


class Business(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    text = models.CharField(max_length=50)
    taxid = models.CharField(max_length=15)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    city = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, blank=True, default='')
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    description = models.CharField(max_length=1000)
    rating = models.FloatField(default=0, blank=True, null=True)
    facebook_link = models.CharField(max_length=50, default='', blank=True)
    twitter_link = models.CharField(max_length=50, default='', blank=True)
    instagram_link = models.CharField(max_length=50, default='', blank=True)
    linkedin_link = models.CharField(max_length=50, default='', blank=True)
    picture1 = models.ImageField(upload_to=upload_profile_image_to)
    picture2 = models.ImageField(upload_to=upload_profile_image_to, null=True, blank=True)
    picture3 = models.ImageField(upload_to=upload_profile_image_to, null=True, blank=True)
    picture4 = models.ImageField(upload_to=upload_profile_image_to, null=True, blank=True)

    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(SubCategory)

    customer_token = models.CharField(max_length=50, default='', blank=True)
    
    security_hash = models.CharField(max_length=32, default='', blank=True)
    ssn_token = models.CharField(max_length=10, default='', blank=True)

    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.text+' ('+self.account.first_name+' '+self.account.last_name+')'

    def get_images(self):
        images = BusinessImage.objects.filter(business=self).order_by('-created_at')
        return images

    def get_billing_info(self):
        billing_info = BusinessBillingInfo.objects.get(business=self)
        return billing_info

class BusinessBillingInfo(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    active = models.BooleanField(default=0)

    type = models.CharField(max_length=10) # bank, debit, mail
    text = models.CharField(max_length=4)
    token = models.CharField(max_length=70)

    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    zip = models.CharField(max_length=20)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40, default='', blank=True)

    def __str__(self):
        return self.business.text+' ('+self.type+', '+self.text+')'
        