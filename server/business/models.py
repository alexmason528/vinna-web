from django.db import models

class Category(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Business(models.Model):
    account = models.OneToOneField('account.Account', on_delete=models.CASCADE)

    text = models.CharField(max_length=50)
    taxid = models.CharField(max_length=15)
    country = models.ForeignKey('core.Country')
    state = models.ForeignKey('core.State')
    zip = models.CharField(max_length=20)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    facebook_link = models.CharField(max_length=50, null=True, blank=True)
    twitter_link = models.CharField(max_length=50, null=True, blank=True)
    instagram_link = models.CharField(max_length=50, null=True, blank=True)
    linkedin_link = models.CharField(max_length=50, null=True, blank=True)

    category = models.ForeignKey(Category)
    sub_category = models.ForeignKey(SubCategory)

    security_hash = models.CharField(max_length=32)
    ssn_token = models.CharField(max_length=10)

    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.text+' ('+self.account.first_name+' '+self.account.last_name+')'

class BusinessBillingInfo(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

    active = models.BooleanField();

    type = models.CharField(max_length=10) # bank, debit, mail
    text = models.CharField(max_length=5)
    token = models.CharField(max_length=70)

    country = models.ForeignKey('core.Country')
    state = models.ForeignKey('core.State')
    zip = models.CharField(max_length=20)
    address1 = models.CharField(max_length=40)
    address2 = models.CharField(max_length=40)

    def __str__(self):
        return self.business.text+' ('+self.type+', '+self.text+')'
        