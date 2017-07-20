import hashlib
import string

from rest_framework import serializers

from server.media.serializers import BusinessImageSerializer

from .models import Notification

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class NotificationSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False, allow_blank=True)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    account_id = serializers.IntegerField(required=False)
    business_id = serializers.IntegerField()
    picture = Base64ImageField(max_length=None, use_url=True)


    class Meta:
        model = Notification
        fields = ('title', 'category', 'description', 'state', 'link', 'start', 'end', 'account_id', 'business_id', 'picture')
        ordering = ['-create_date']
