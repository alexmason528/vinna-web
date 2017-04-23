from django.db import models

# Create your models here.
class Language(models.Model):
  code = models.CharField(max_length=4)
  text = models.CharField(max_length=50)
  english_text = models.CharField(max_length=50)

  def __str__(self):
    return self.text


class Country(models.Model):        
  phone_country_code = models.CharField(max_length=5)
  abbrev = models.CharField(max_length=5)
  text = models.CharField(max_length=50)
  english_text = models.CharField(max_length=50)
  default_language = models.ForeignKey(Language)

  def __str__(self):
    return self.english_text

class State(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  abbrev = models.CharField(max_length=5)
  text = models.CharField(max_length=50)
  language = models.ForeignKey(Language)

  def __str__(self):
    return self.text
