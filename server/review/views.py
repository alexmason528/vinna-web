from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Review
from .serializers import ReviewSerializer

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
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['GET','PUT', 'DELETE'])
	def review_element(request, id):
		review = get_object_or_404(Review, pk=id)
		if request.user.account.id != review.account.id:
			raise PermissionDenied
		
		if request.method == 'GET':	
			serializer = ReviewSerializer(review)
			return Response(serializer.data)

		elif request.method == 'PUT':
			serializer = ReviewSerializer(review, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			review.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)
