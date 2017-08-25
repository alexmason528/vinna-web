import base64

from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings
from server.account.models import Account

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

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

def UserAuthMiddleware(get_response):
    def middleware(request):
        authorization = request.META.get('HTTP_AUTHORIZATION')
        if not authorization:
            return get_response(request)

        headers = authorization.split(',')

        if (len(headers) == 1):
            return get_response(request)

        (jwt_token, auth_param) = headers

        jwt_token = jwt_token.replace('JWT ', '')
        payload = jwt_decode_handler(jwt_token, request)

        (name, value) = auth_param.split(' ')

        if (name == 'account_id'):
            account = None
            try:
                account = get_object_or_404(Account, id=value)
            except:
                response = HttpResponse('Unauthorized')
                response.status_code = 401
                return response

            if account:
                if account.user.id != payload['user_id']:
                    response = HttpResponse('Unauthorized')
                    response.status_code = 401
                    return response

        request.META['HTTP_AUTHORIZATION'] = headers[0]
        return get_response(request)
    return middleware 
