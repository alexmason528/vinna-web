import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer

class NotificationView(APIView):

	@api_view(['GET', 'POST'])
	def notification_collection(request):
		if request.method == 'GET':
			notifications = Notification.objects.filter(end__gte=datetime.datetime.utcnow()).order_by('-start')
			serializer = NotificationSerializer(notifications, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = NotificationSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['GET','PUT', 'DELETE'])
	def notification_element(request, id):
		notification = get_object_or_404(Notification, pk=id)

		if request.method == 'GET':	
			serializer = NotificationSerializer(notification)
			return Response(serializer.data)

		elif request.method == 'PUT':
			serializer = NotificationSerializer(notification, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			notification.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)
