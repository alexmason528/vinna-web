from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image, Video, BusinessImage, BusinessVideo
from .serializers import ImageSerializer, VideoSerializer, BusinessImageSerializer, BusinessVideoSerializer

class ImageView(APIView):

	@api_view(['GET', 'POST'])
	def image_collection(request):
		if request.method == 'GET':
			images = Image.objects.all()
			serializer = ImageSerializer(images, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = ImageSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET', 'DELETE'])
	def image_element(request, id):
		if request.method == 'GET':	
			image = get_object_or_404(Image, pk=id)
			serializer = ImageSerializer(image)
			return Response(serializer.data)

		elif request.method == 'PUT':
			image = get_object_or_404(Image, pk=id)
			serializer = ImageSerializer(image, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			image = get_object_or_404(Image, pk=id)
			image.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)

class BusinessImageView(APIView):

	@api_view(['GET', 'POST'])
	def business_image_collection(request):
		if request.method == 'GET':
			bimages = BusinessImage.objects.all()
			serializer = BusinessImageSerializer(bimages, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = BusinessImageSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET', 'DELETE'])
	def business_image_element(request, id):
		if request.method == 'GET':	
			bimage = get_object_or_404(BusinessImage, pk=id)
			serializer = BusinessImageSerializer(bimage)
			return Response(serializer.data)

		elif request.method == 'PUT':
			bimage = get_object_or_404(BusinessImage, pk=id)
			serializer = BusinessImageSerializer(bimage, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			bimage = get_object_or_404(BusinessImage, pk=id)
			bimage.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)


class VideoView(APIView):

	@api_view(['GET', 'POST'])
	def video_collection(request):
		if request.method == 'GET':
			videos = Video.objects.all()
			serializer = VideoSerializer(videos, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = VideoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET', 'DELETE'])
	def video_element(request, id):
		if request.method == 'GET':	
			video = get_object_or_404(Video, pk=id)
			serializer = VideoSerializer(video)
			return Response(serializer.data)

		elif request.method == 'PUT':
			video = get_object_or_404(Video, pk=id)
			serializer = VideoSerializer(video, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			video = get_object_or_404(Video, pk=id)
			video.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)

class BusinessVideoView(APIView):

	@api_view(['GET', 'POST'])
	def business_video_collection(request):
		if request.method == 'GET':
			bvideos = BusinessVideo.objects.all()
			serializer = BusinessVideoSerializer(bvideos, many=True)
			return Response(serializer.data)
		
		elif request.method == 'POST':
			serializer = BusinessVideoSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				raise ValidationError(detail={'error': serializer.errors})

	@api_view(['PUT','GET', 'DELETE'])
	def business_video_element(request, id):
		if request.method == 'GET':	
			bvideo = get_object_or_404(BusinessVideo, pk=id)
			serializer = BusinessVideoSerializer(bvideo)
			return Response(serializer.data)

		elif request.method == 'PUT':
			bvideo = get_object_or_404(BusinessVideo, pk=id)
			serializer = BusinessVideoSerializer(bvideo, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				raise ValidationError(detail={'error': serializer.errors})

		elif request.method == 'DELETE':
			bvideo = get_object_or_404(BusinessVideo, pk=id)
			bvideo.delete()
			return Response({'detail': 'Deleted'}, status=status.HTTP_200_OK)
