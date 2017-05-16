from django.test import TestCase
from server.media.models import Image, Video, BusinessImage, BusinessVideo

class ImageTestCase(TestCase):
	def setUp(self):
		Image.objects.create(hash='image_hash', s3_url='image_s3_url', title='image_title', description='image_description')

	def test_image(self):
		Image = Image.objects.get(hash='image_hash')
		self.assertEqual(Image.hash, 'image_hash')
		self.assertEqual(Image.s3_url, 'image_s3_url')
		self.assertEqual(Image.title, 'image_title')
		self.assertEqual(Image.description, 'image_description')

class VideoTestCase(TestCase):
	def setUp(self):
		Video.objects.create(hash='image_hash', s3_url='image_s3_url', title='image_title', description='image_description')

	def test_video(self):

		pass
