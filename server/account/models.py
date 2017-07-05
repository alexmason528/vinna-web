import qrcode
import base64
import io
import jwt

from django.db import models
from django.conf import settings

from core.models import Language
# from server.member.models import Member

def upload_profile_image_to(instance, filename):
    import os
    from django.utils.timezone import now

    filename_base, filename_ext = os.path.splitext(filename)
    return 'profile/%s/%s%s' % (
        now().strftime("%Y%m%d"),
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    dob = models.DateField()
    gender = models.CharField(choices=((u'F',u'Female'),(u'M',u'Male')), max_length=1)
    profile_photo_url = models.ImageField(upload_to=upload_profile_image_to, null=True, blank=True)
    referral_member = models.ForeignKey('member.Member', related_name='member_referral', null=True, blank=True)
    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)

    def __str__(self):
        return self.first_name+' '+self.last_name


    def get_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        
        qr.add_data(jwt.encode({'id': self.id}, 'secret').decode('utf-8'))
        qr.make(fit=True)

        img = qr.make_image()

        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format = "PNG")
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()

        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
        return base64_encoded_result_str
