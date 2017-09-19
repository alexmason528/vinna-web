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

from .models import Review
from .serializers import ReviewSerializer

@permission_classes(IsAuthenticated, )
@authentication_classes(CustomJSONWebTokenAuthentication, )

class ReviewView(APIView):

	@api_view(['GET', 'POST'])
	def review_collection(request):
		if request.method == 'GET':
			reviews = Review.objects.all()
			serializer = ReviewSerializer(reviews, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = ReviewSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@api_view(['GET','PUT', 'DELETE'])
	def review_element(request, id):
		if request.method == 'GET':	
			review = get_object_or_404(Review, pk=id)
			serializer = ReviewSerializer(review)
			return Response(serializer.data)

		elif request.method == 'PUT':
			review = get_object_or_404(Review, pk=id)
			serializer = ReviewSerializer(review, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			review = get_object_or_404(Review, pk=id)
			review.delete()
