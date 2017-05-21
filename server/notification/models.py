from django.db import models

# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    state = models.BooleanField(default=0)

    def __str__(self):
    	return self.title
    	