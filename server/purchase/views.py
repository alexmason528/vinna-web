from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from .models import Purchase
from .serializers import PurchaseSerializer

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class PurchaseView(APIView):

	@api_view(['GET', 'POST'])
	def purchase_collection(request):
		if request.method == 'GET':
			puchases = Purchase.objects.all()
			serializer = PurchaseSerializer(puchases, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = PurchaseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def purchase_element(request, id):
		if request.method == 'GET':	
			account = get_object_or_404(Account, pk=id)
			serializer = PurchaseSerializer(account)
			return Response(serializer.data)

		elif request.method == 'PUT':
			serializer = PurchaseSerializer(account, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
