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

from .models import CreditCard, BankAccount, Customer
from .serializers import CreditCardSerializer, BankAccountSerializer, CustomerSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class CustomerView(APIView):

	@api_view(['GET', 'POST'])
	def customer_collection(request):
		pass

	@api_view(['GET','PUT', 'DELETE'])
	def customer_element(request, id):
		pass

class BankAccountView(APIView):

	@api_view(['GET', 'POST'])
	def bankaccount_collection(request):
		pass

	@api_view(['GET','PUT', 'DELETE'])
	def bankaccount_element(request, id):
		pass

class CreditCardView(APIView):

	@api_view(['GET', 'POST'])
	def creditcard_collection(request):
		pass

	@api_view(['GET','PUT', 'DELETE'])
	def creditcard_element(request, id):
		pass
