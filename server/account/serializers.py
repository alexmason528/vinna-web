import random

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from rest_framework import serializers
from core.serializers import UserSerializer
from server.account.partner_model import AccountPartnerRole
from server.business.invitation_model import Invitation
from server.account.models import AccountReferral
from .models import Account

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

class AccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    qrcode = serializers.CharField(source='get_qrcode', read_only=True)
    profile_photo_url = Base64ImageField(max_length=None, use_url=True)
    registration_link = serializers.CharField(source='get_registration_link', read_only=True)
    email_status = serializers.BooleanField(source='get_email_status', read_only=True)
    phone_status = serializers.BooleanField(source='get_phone_status', read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'first_name','last_name', 'email', 'phone', 'dob', 'gender', 'password', 'profile_photo_url', 'qrcode', 'registration_link', 'email_status', 'phone_status')

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        if User.objects.filter(username=email).count() > 0:
            raise ValidationError("Email is already taken by other account")

        if Account.objects.filter(phone=validated_data['phone']).count() > 0:
            raise ValidationError("Phone number is already taken by other account")

        invitation = None

        try:
            invitation = Invitation.objects.get(email=email)
        except:
            pass
        
        user_info = {
            'first_name' : validated_data['first_name'],
            'last_name' : validated_data['last_name'],
            'username' : email,
            'is_superuser' : 0,
            'is_staff' : 0,
            'is_active' : 1,
            'email' : email,
            'password' : make_password(password)
        }

        referral = None
        try:
            referral = AccountReferral.objects.get(Q(friend_email_or_phone=email) | Q(friend_email_or_phone=validated_data['phone']))  
        except:
            pass

        if referral:
            referral.connected = 1
            referral.save()

        user = User.objects.create(**user_info)
        validated_data['language_id'] = 1

        email_code = random.randint(1000, 9999)
        phone_code = random.randint(1000, 9999)

        validated_data['email_verified'] = email_code
        validated_data['phone_verified'] = phone_code

        account = Account.objects.create(user_id=user.id, **validated_data)

        if invitation:
            partner_role_info = {
                'account_id': account.id,
                'business_id': invitation.business_id,
                'role': 'cashier',
                'description': 'extra'
            }
            AccountPartnerRole.objects.create(**partner_role_info)

        mail_content = 'Please verify your email address. Verification code: ' + str(email_code)

        try:
            send_mail(
                'Thanks for using Vinna app',
                mail_content,
                'tech@vinna.me',
                [email],
                fail_silently=False,
            )
        except:
            pass

        return account

    def update(self, instance, validated_data):

        user = instance.user

        if 'first_name' in validated_data:
            setattr(user, 'first_name', validated_data['first_name'])

        if 'last_name' in validated_data:
            setattr(user, 'last_name', validated_data['last_name'])

        if 'email' in validated_data:
            email = validated_data.pop('email')
            setattr(user, 'email', email)
            setattr(user, 'username', email)

        if 'password' in validated_data:
            setattr(user, 'password', make_password(validated_data.pop('password')))

        user.save()

        for item in validated_data:
            if Account._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        instance.save()
        return instance
