from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from vinna.authentication import CustomJSONWebTokenAuthentication

from .models import Notification
from .serializers import NotificationSerializer

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

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
