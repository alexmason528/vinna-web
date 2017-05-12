# builtin
import base64
import json
import jwt
# django
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.core.urlresolvers import resolve

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from core.models import UserLog
from django.core.exceptions import ObjectDoesNotExist
from ipware.ip import get_real_ip, get_ip
from rest_framework import exceptions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def _unauthed():
    response = HttpResponse('''
        <html><title>Authorization required</title><body>
        <h1>Authorization Required</h1></body></html>
    ''')
    response['WWW-Authenticate'] = 'Basic realm=""'
    response.status_code = 401
    return response

def _valid_login(auth):
    username, password = base64.b64decode(auth).decode('utf-8').split(':', 1)
    if not username == settings.BASICAUTH_USERNAME:
        return False
    if not password == settings.BASICAUTH_PASSWORD:
        return False
    return True


def basic_auth_middleware(get_response):

    def middleware(request):

        if not request.META.get('HTTP_AUTHORIZATION'):
            return _unauthed()

        else:
            auth = request.META['HTTP_AUTHORIZATION'].split(' ',1)

            if 'basic' != auth[0].lower():
                return _unauthed()
            if _valid_login(auth[1]):
                return get_response(request)
            else:
                return _unauthed()

    return middleware

def disable_csrf_middleware(get_response):
    def middleware(request):
        resolved_app_name = resolve(request.path_info).app_name

        app_name = "accounts_api"
        if resolved_app_name == app_name:
            setattr(request, '_dont_enforce_csrf_checks', True)
        app_name = "members_api"
        if resolved_app_name == app_name:
            setattr(request, '_dont_enforce_csrf_checks', True)
        app_name = "business_api"
        if resolved_app_name == app_name:
            setattr(request, '_dont_enforce_csrf_checks', True)
        return get_response(request)

    return middleware

def authenticate_jwt(get_response):
    def middleware(request):
        if ((request.POST.get('username') is not None) & (request.POST.get('password') is not None)):
            credentials = {
                'username': request.POST['username'],
                'password': request.POST['password']
            }

            user = authenticate(**credentials)

            if user:
                if user.is_active:
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)

                    ip = get_ip(request)

                    userlog = None
                    try:
                        userlog = UserLog.objects.get(user_id=user.id)
                    except ObjectDoesNotExist:
                        pass

                    if userlog is None:
                        log = UserLog(user_id=user.id, ip=ip, current_token=token)     
                        log.save()
                    else:
                        userlog.current_token = token
                        userlog.ip = ip
                        userlog.save()
        else:
            auth = request.META.get('HTTP_AUTHORIZATION')
            prefix, token = auth.split(' ');
            ip = get_ip(request)
            ip ='123.123.123.123'
            userlog = UserLog.objects.get(current_token=token)
            if ip != userlog.ip:
                msg = 'User account is disabled.'
                raise exceptions.AuthenticationFailed(msg)

        return get_response(request)

    return middleware
