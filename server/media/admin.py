from django.contrib import admin
from .models import Image, Video, BusinessImage, BusinessVideo

# Register your models here.
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(BusinessImage)
admin.site.register(BusinessVideo)
