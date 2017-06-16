from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from core.serializers import UserSerializer
from server.account.partner_model import AccountPartnerRole
from server.account.partner_serializer import AccountPartnerRoleSerializer
from server.business.invitation_model import Invitation
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

    profile_photo_url = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'first_name','last_name', 'email', 'phone', 'dob', 'gender', 'password', 'profile_photo_url')

    def create(self, validated_data):

        invitation = None

        try:
            invitation = Invitation.objects.get(email=validated_data['email'])
        except:
            pass

        
        user_info = {
            'first_name' : validated_data['first_name'],
            'last_name' : validated_data['last_name'],
            'username' : validated_data['email'],
            'is_superuser' : 0,
            'is_staff' : 0,
            'is_active' : 1,
            'email' : validated_data.pop('email'),
            'password' : make_password(validated_data.pop('password'))
        }

        serializer = UserSerializer(data=user_info)
        if serializer.is_valid():
            serializer.save()

        validated_data['language_id'] = 1

        account = Account.objects.create(user_id=serializer.data['id'], **validated_data)

        if invitation:
            serializer = AccountPartnerRoleSerializer(data={'account_id': account.id, 'business_id': invitation.business_id, 'role': 'cashier', 'description': 'extra'})
            if serializer.is_valid():
                serializer.save()

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
