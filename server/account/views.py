from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from .models import Account
from core.models import Language
from .serializers import AccountSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token


@permission_classes((IsAuthenticated,))
class AccountView(APIView):


    @api_view(['GET'])
    def account_detail(request, userid):
        if request.user.id != int(userid):
            userid = -1

        user = get_object_or_404(User, id=userid)
        account = get_object_or_404(Account, user=user)

#        try:
#            user = User.objects.get(id=userid)
#        except User.DoesNotExist:
#            return HttpResponse(status=404)

        serializer = AccountSerializer(account, context={'request': request})

        return JsonResponse(serializer.data)
