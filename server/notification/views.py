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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from rest_framework.authtoken.models import Token

@permission_classes(IsAuthenticated, )
@authentication_classes(JSONWebTokenAuthentication, )

class NotificationView(APIView):

	@api_view(['GET', 'POST'])
	def notification_collection(request):
		if request.method == 'GET':
			notifications = Notification.objects.all()
			serializer = NotificationSerializer(notifications, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = NotificationSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET','PUT', 'DELETE'])
	def notification_element(request, id):
		if request.method == 'GET':	
			notification = get_object_or_404(Notification, pk=id)
			serializer = NotificationSerializer(notification)
			return Response(serializer.data)

		elif request.method == 'PUT':
			notification = get_object_or_404(Notification, pk=id)
			serializer = NotificationSerializer(notification, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			notification = get_object_or_404(Notification, pk=id)
			notification.delete()
