import jwt
import uuid
import warnings
import requests
import os

from django.http import HttpResponse, HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions

from ipware.ip import get_real_ip, get_ip
from core.models import UserLog
from socket import gethostname, gethostbyname 
from bottle import request



def get_secret_key(payload=None):
    """
    For enchanced security you may use secret key on user itself.
    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if api_settings.JWT_GET_USER_SECRET_KEY:
        User = get_user_model()  # noqa: N806
        user = User.objects.get(pk=payload.get('user_id'))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key
    return api_settings.JWT_SECRET_KEY

def payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)
    print(os.environ) 
    
    ip = '127.0.0.1'
    
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

    # Include original issued at time for a brand new token,
    # to allow token refresh
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

def decode_handler(token):
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    # get user from token, BEFORE verification, to get user secret key
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
    current_ip = '127.0.0.1'


    if token_ip != current_ip:
        raise exceptions.AuthenticationFailed('Invalid token')

    return decoded_token