from django.db import models

# Create your models here.
class Category(models.Model):
  text = models.CharField(max_length=50)


class SubCategory(models.Model):
  category = models.ForeignKey(Category)
  text = models.CharField(max_length=50)  

class Business(models.Model):
  account = models.ForeignKey('account.Account')

  text = models.CharField(max_length=50)
  taxid = models.CharField(max_length=15)
  country = models.ForeignKey('core.Country')
  state = models.ForeignKey('core.State')
  zip = models.CharField(max_length=20)
  address1 = models.CharField(max_length=40)
  address2 = models.CharField(max_length=40)
  email = models.CharField(max_length=50)
  phone = models.CharField(max_length=25)

  category = models.ForeignKey(Category)
  sub_category = models.ForeignKey(SubCategory)

  security_hash = models.CharField(max_length=32)
  ssn_token = models.CharField(max_length=10)

  last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

class BusinessSocial(models.Model):
  business = models.ForeignKey(Business)

  facebook_link = models.CharField(max_length=50)
  twitter_link = models.CharField(max_length=50)
  instagram_link = models.CharField(max_length=50)
  linkedin_link = models.CharField(max_length=50)


class BusinessBillingInfo(models.Model):
  business = models.ForeignKey(Business)

  active = models.BooleanField();

  type = models.CharField(max_length=10) # bank, debit, mail
  text = models.CharField(max_length=5)
  token = models.CharField(max_length=70)

  country = models.ForeignKey('core.Country')
  state = models.ForeignKey('core.State')
  zip = models.CharField(max_length=20)
  address1 = models.CharField(max_length=40)
  address2 = models.CharField(max_length=40)