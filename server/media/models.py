from django.db import models
from server.business.models import Business

class Image(models.Model):
    hash = models.CharField(max_length=100)
    s3_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.title

class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete = models.CASCADE)
    hash = models.CharField(max_length=100)
    s3_url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    link = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=100, unique=True)
    platform = models.CharField(choices=((u'Y',u'Youtube'),(u'V',u'Vimeo')), max_length=1)

    def __str__(self):
        return self.unique_code

class BusinessVideo(models.Model):
    business = models.ForeignKey(Business, on_delete = models.CASCADE)
    link = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=100, unique=True)
    platform = models.CharField(choices=((u'Y',u'Youtube'),(u'V',u'Vimeo')), max_length=1)

    def __str__(self):
        return self.unique_code
        