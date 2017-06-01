from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from .models import Account, Role, AccountRole

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class AccountRoleSerializer(serializers.HyperlinkedModelSerializer):
    role_id = serializers.ReadOnlyField(source='role.id')
    account_id = serializers.ReadOnlyField(source='account.id')

    class Meta:
        model = AccountRole
        fields = ('role_id', 'account_id')

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description')

class AccountListSerializer(serializers.HyperlinkedModelSerializer):
    roles = RoleSerializer(many=True)
    language_id = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'roles')

class AccountCreateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    roles = serializers.PrimaryKeyRelatedField(many=True, write_only=True, required=False, queryset = Role.objects.all())
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    profile_photo_url = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'first_name','last_name', 'email', 'phone', 'dob', 'gender', 'password', 'profile_photo_url', 'roles')

    def create(self, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')

        user_info = {}
        user_info['first_name'] = validated_data['first_name']
        user_info['last_name'] = validated_data['last_name']
        user_info['username'] = validated_data['first_name'] + validated_data['last_name']
        user_info['is_superuser'] = 0
        user_info['is_staff'] = 0
        user_info['is_active'] = 1
        user_info['email'] = validated_data['email']
        user_info['password'] = make_password(validated_data['password'])

        user = User.objects.create(**user_info)
        
        validated_data.pop('email')
        validated_data.pop('password')

        validated_data['language_id'] = 1

        account = Account.objects.create(user=user, **validated_data)

        if roles is not None:
            for role in roles:
                AccountRole.objects.create(account=account, role=role)

        return account

    def update(self, instance, validated_data):

        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')

        user = instance.user

        setattr(user, 'first_name', validated_data['first_name'])
        setattr(user, 'last_name', validated_data['last_name'])
        setattr(user, 'email', validated_data['email'])
        setattr(user, 'password', make_password(validated_data['password']))
        setattr(user, 'username', validated_data['first_name'] + validated_data['last_name'])

        user.save()

        validated_data.pop('email')
        validated_data.pop('password')

        for item in validated_data:
            if Account._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        if roles is not None:
            AccountRole.objects.filter(account=instance).delete()
            for role in roles:
                AccountRole.objects.create(account=instance, role=role)
        instance.save()
        return instance
