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

class Image(models.Model):
    hash = models.CharField(max_length=100)
    s3_url = models.ImageField(upload_to=upload_profile_image_to, default='', blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.title

class BusinessImage(models.Model):
    business = models.ForeignKey('business.Business', on_delete = models.CASCADE)
    hash = models.CharField(max_length=100)
    s3_url = models.ImageField(upload_to=upload_profile_image_to, default='', blank=True)
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField('Created At', auto_now=True)
    type = models.CharField(max_length=12)
    def __str__(self):
        return self.title

class Video(models.Model):
    link = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=100, unique=True)
    platform = models.CharField(choices=((u'Y',u'Youtube'),(u'V',u'Vimeo')), max_length=1)

    def __str__(self):
        return self.unique_code

class BusinessVideo(models.Model):
    business = models.OneToOneField('business.Business', on_delete = models.CASCADE)
    link = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=100, unique=True)
    platform = models.CharField(choices=((u'Y',u'Youtube'),(u'V',u'Vimeo')), max_length=1)

    def __str__(self):
        return self.unique_code
        