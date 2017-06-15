from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from server.business.models import Business
from server.business.serializers import BusinessSerializer
from server.media.models import BusinessImage

from server.media.serializers import BusinessImageSerializer

from .models import Account
from .serializers import AccountSerializer

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
	def account_element(request, id):
		if request.method == 'GET':	
			account = get_object_or_404(Account, pk=id)
			serializer = AccountSerializer(account)
			return Response(serializer.data)

		elif request.method == 'PUT':
			account = get_object_or_404(Account, pk=id)

			if ('current_password' in request.data) and ('username' in request.data):
				credentials = {
					'username': request.data['username'],
					'password': request.data['current_password']
				}

				user = authenticate(**credentials)

				if not user:
					return Response('Current password is wrong', status=status.HTTP_400_BAD_REQUEST)

				request.data.pop('current_password')
				request.data.pop('username')

			serializer = AccountSerializer(account, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET'])
	def nearest_partner(request, id):
		if request.method == 'GET':
			businesses = Business.objects.filter(account_id=id).order_by('-last_modified_date')
			serializer = BusinessSerializer(businesses, many=True)
			
			for business in serializer.data:
				business_image = BusinessImage.objects.filter(business_id=business['id']).order_by('-created_at').first()
				business_image_serializer = BusinessImageSerializer(business_image)
				business['image'] = business_image_serializer.data

			return Response(serializer.data)