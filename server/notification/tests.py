from django.test import TestCase
from server.notification.models import Notification

class NotificationTestCase(TestCase):
	def setUp(self):
		Notification.objects.create(title='Scheduled Maintenance', category='Notice', message='We are going to take a scheduled maintenance on May, 16 from 8 AM to 12PM')

	def test_notification(self):
		notification = Notification.objects.get(category='Notice')
		self.assertEqual(notification.title, 'Scheduled Maintenance')
		self.assertEqual(notification.category, 'Notice')
		self.assertEqual(notification.message, 'We are going to take a scheduled maintenance on May, 16 from 8 AM to 12PM')
