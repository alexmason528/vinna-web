from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Account, Role, AccountRole
from django.shortcuts import get_object_or_404

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

            # Try to decode the file. Return validation error if it fails.
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
    user_id = serializers.IntegerField()
    language_id = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('user_id', 'first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'roles')

class AccountCreateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    roles = serializers.PrimaryKeyRelatedField(many=True, write_only=True, required=False, queryset = Role.objects.all())
    user_id = serializers.IntegerField()
    language_id = serializers.IntegerField()
    profile_photo_url = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Account
        fields = ('id', 'user_id', 'first_name','last_name', 'language_id', 'phone', 'dob', 'gender', 'profile_photo_url', 'roles')

    def create(self, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')
        account = Account.objects.create(**validated_data)
        if roles is not None:
            for role in roles:
                AccountRole.objects.create(account=account, role=role)
        return account

    def update(self, instance, validated_data):
        roles = None
        if 'roles' in validated_data:
            roles = validated_data.pop('roles')
        for item in validated_data:
            if Account._meta.get_field(item):
                setattr(instance, item, validated_data[item])

        if roles is not None:
            AccountRole.objects.filter(account=instance).delete()
            for role in roles:
                AccountRole.objects.create(account=instance, role=role)
        instance.save()
        return instance
