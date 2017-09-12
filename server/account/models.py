import qrcode
import base64
import io
import jwt
import short_url

from django.db import models
from django.conf import settings

from core.models import Language

from vinna.settings import BASE_URL

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
    phone = models.CharField(default='', max_length=25)
    dob = models.DateField()
    gender = models.CharField(choices=((u'F',u'Female'),(u'M',u'Male')), max_length=1)
    country = models.ForeignKey('core.Country', default=1)
    profile_photo_url = models.ImageField(upload_to=upload_profile_image_to)
    referral_account = models.ForeignKey('Account', related_name='account_referral', null=True, blank=True)
    last_modified_date = models.DateTimeField('Last Modified', auto_now=True)
    email_verified = models.CharField(default='0', max_length=50)
    new_email = models.CharField(default='', max_length=50)
    new_phone = models.CharField(default='', max_length=50)
    new_email_verified = models.CharField(default='0', max_length=50)
    new_phone_verified = models.CharField(default='0', max_length=50)

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

    def get_registration_link(self):
        link = short_url.encode_url(self.id)
        return BASE_URL + 'app/?code=' + str(link)

    def is_email_verified(self):
        if self.new_email and self.new_email_verified == '1':
            return True
        elif not self.new_email and self.email_verified == '1':
            return True
        return False

    def is_phone_verified(self):
        if self.new_phone and self.new_phone_verified == '1':
            return True
        return False


class AccountReferral(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    friend_email_or_phone = models.CharField(max_length=40)
    friend_ip = models.CharField(max_length=45, null=True, blank=True)
    friend_user_agent = models.CharField(max_length=200, null=True, blank=True)
    friend_referrer = models.CharField(max_length=200, null=True, blank=True)
    connected = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now=True)
