from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from vinna.authentication import CustomJSONWebTokenAuthentication
from rest_framework.views import APIView

from .models import Account, AccountPartnerRole
from core.models import Language
from .serializers import AccountSerializer, AccountPartnerRoleSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class AccountView(APIView):

	@api_view(['GET', 'POST'])
	def account_collection(request):
		if request.method == 'GET':
			accounts = Account.objects.all()
			serializer = AccountSerializer(accounts, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = AccountSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def account_element(request, userid):
		if request.method == 'GET':	
			account = get_object_or_404(Account, pk=userid)
			serializer = AccountSerializer(account)
			return Response(serializer.data)

		elif request.method == 'PUT':
			account = get_object_or_404(Account, pk=userid)
			serializer = AccountSerializer(account, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

