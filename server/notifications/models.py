from django.db import models

# Create your models here.

class Notification(models.Model):
#  language = models.ForeignKey(Language) # No Language setting per Registration nor Member. Detect from browser or device.
  title = models.CharField(max_length=140)
  category = models.CharField(max_length=50)
  message = models.CharField(max_length=1000)
#  image1 = models.ForeignKey('Media.Image')
#  start_date = models.CharField(max_length=40)
#  end_date = models.CharField(max_length=40)
#  image2 = 
#  image3 = 
#  image4 =   