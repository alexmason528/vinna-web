# Create your models here.
from django.db import models



class Language(models.Model):
  language_code = models.CharField(max_length=4)
  language = models.CharField(max_length=50)


class Country(models.Model):
  phone_code = models.CharField(max_length=5)
  abbrev = models.CharField(max_length=5)
  name = models.CharField(max_length=50)
  language = models.ForeignKey(Language)

class State(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  abbrev = models.CharField(max_length=5)
  name = models.CharField(max_length=50)
  language = models.ForeignKey(Language)



class Registration(models.Model):
  
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=1)
  language = models.ForeignKey(Language)

  profile_photo_url = models.CharField(max_length=100)

  email1 = models.CharField(max_length=100)
  email2 = models.CharField(max_length=100)
  
  phone = models.CharField(max_length=25)

  mailing_address_1 = models.CharField(max_length=40)
  mailing_address_2 = models.CharField(max_length=40)
  mailing_address_city = models.CharField(max_length=50)
  mailing_address_state = models.ForeignKey(State)
  mailing_address_zip = models.CharField(max_length=20)
  mailing_address_country = models.ForeignKey(Country)


  payment_method = models.CharField(max_length=10)
  payment_token = models.CharField(max_length=70)

#  payment_address_1 = models.CharField(max_length=40)
#  payment_address_2 = models.CharField(max_length=40)
#  payment_address_city = models.CharField(max_length=50)
#  payment_address_state = models.ForeignKey(State)
#  payment_address_zip = models.CharField(max_length=20)
#  payment_address_country = models.ForeignKey(Country)


  security_hash = models.CharField(max_length=32)
  birthdate = models.DateTimeField('birth date')
  ssn_token = models.CharField(max_length=10)


class Member(models.Model):
  name = models.CharField(max_length=100)
  gender = models.CharField(max_length=1)
  language = models.ForeignKey(Language)

  profile_photo_url = models.CharField(max_length=100)

  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=25)

  mailing_address_1 = models.CharField(max_length=40)
  mailing_address_2 = models.CharField(max_length=40)
  mailing_address_city = models.CharField(max_length=50)
  mailing_address_state = models.ForeignKey(State)
  mailing_address_zip = models.CharField(max_length=20)
  mailing_address_country = models.ForeignKey(Country)

  payment_method = models.CharField(max_length=10)
  payment_text = models.CharField(max_length=5)
  payment_token = models.CharField(max_length=70)


#  payment_address_1 = models.CharField(max_length=40)
#  payment_address_2 = models.CharField(max_length=40)
#  payment_address_city = models.CharField(max_length=50)
#  payment_address_state = models.ForeignKey(State)
#  payment_address_zip = models.CharField(max_length=20)
#  payment_address_country = models.ForeignKey(Country)

  
  security_hash = models.CharField(max_length=32)
  birthdate = models.DateTimeField('birth date')
  ssn_token = models.CharField(max_length=10)


class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

