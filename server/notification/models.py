from django.utils import timezone
from django.db import models

def upload_profile_image_to(instance, filename):
    import os
    from django.utils.timezone import now

    filename_base, filename_ext = os.path.splitext(filename)
    return 'profile/%s/%s%s' % (
        now().strftime("%Y%m%d"),
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )

class Notification(models.Model):
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=140)
    state = models.BooleanField(default=0)
    link = models.CharField(max_length=150, blank=True, default='')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    business = models.ForeignKey('business.Business')
    account = models.ForeignKey('account.Account', blank=True, null=True)
    picture = models.ImageField(upload_to=upload_profile_image_to)

    def __str__(self):
    	return self.title

    
