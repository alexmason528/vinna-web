from django.db import models
from django.conf import settings

class UserLog(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    last_login_time = models.DateTimeField('Last Login Time', auto_now=True)
    current_token = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username

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
        return self.english_text + ' (' + self.abbrev + ')'

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    abbrev = models.CharField(max_length=5)
    text = models.CharField(max_length=50)
    language = models.ForeignKey(Language)

    def __str__(self):
        return self.text + ' (' + self.abbrev + ')'
