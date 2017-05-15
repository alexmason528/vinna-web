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

from .models import Member
from .serializers import MemberSerializer

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class MemberView(APIView):

	@api_view(['GET', 'POST'])
	def member_collection(request):
		if request.method == 'GET':
			members = Member.objects.all()
			serializer = MemberSerializer(members, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = MemberSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['PUT','GET'])
	def member_element(request, id):
		if request.method == 'GET':	
			member = get_object_or_404(Member, pk=id)
			serializer = MemberSerializer(member)
			return Response(serializer.data)

		elif request.method == 'PUT':
			member = get_object_or_404(Member, pk=id)
			serializer = MemberSerializer(member, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
