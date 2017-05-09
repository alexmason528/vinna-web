from django.db import models

# Create your models here.

#class Media(models.Model):
#  language = models.ForeignKey(Language) # No Language setting per Registration nor Member. Detect from browser or device.
#  mailing_address_1 = models.CharField(max_length=40)

#class Image(Media):
#  s3url = models.CharField(max_length=100)

#class Video(Media):
#  direct_link = models.CharField(max_length=100)
#  platform = models.CharField(max_length=18)
#  platform_id = models.CharField(max_length=100)

#  embed = models.CharField(max_length=500)
