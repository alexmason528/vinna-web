import jwt
import uuid
import warnings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import exceptions
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings

from calendar import timegm
from datetime import datetime
from ipware.ip import get_real_ip, get_ip

from core.models import UserLog
from server.account.models import Account
from server.member.models import Member

from core.serializers import UserSerializer
from server.account.serializers import AccountListSerializer
from server.member.serializers import MemberSerializer

def get_secret_key(payload=None):
    if api_settings.JWT_GET_USER_SECRET_KEY:
        User = get_user_model()
        user = User.objects.get(pk=payload.get('user_id'))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key
    return api_settings.JWT_SECRET_KEY

def payload_handler(user, request):
    username_field = get_username_field()
    username = get_username(user)
    
    ip = get_ip(request)
    
    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'user_id': user.pk,
        'username': username,
        'ip': ip,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload

def encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or get_secret_key(payload)

    userlog = None

    token = jwt.encode(
        payload,
        key,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')

    try:
        userlog = UserLog.objects.get(user_id=payload['user_id'])
    except ObjectDoesNotExist:
        pass

    if userlog is None:
        log = UserLog(user_id=payload['user_id'], ip=payload['ip'], current_token=token)     
        log.save()
    else:
        userlog.current_token = token
        userlog.ip = payload['ip']
        userlog.save()

    return token

def decode_handler(token, request):
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    
    unverified_payload = jwt.decode(token, None, False)
    secret_key = get_secret_key(unverified_payload)
    decoded_token = jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )

    token_ip = decoded_token['ip']
    current_ip = get_ip(request)

    if token_ip != current_ip:
        raise exceptions.AuthenticationFailed('Invalid token')

    return decoded_token

def response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    Example:
    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
    """

    account, member = None, None
    
    try:
        account = Account.objects.get(user_id = user.id)
        account_id = account.id
    except Account.DoesNotExist:
        pass

    try:
        member = Member.objects.get(account_id = account_id)
        member_id = member.id
    except Member.DoesNotExist:
        pass

    return {
        'token': token,
        'user' : UserSerializer(user).data,
        'account': AccountListSerializer(account).data,
        'member': MemberSerializer(member).data
    }