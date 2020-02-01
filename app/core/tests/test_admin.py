from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse




class AdminTest(TestCase):


	def setUp(self):
		"""Tests for creating users"""
		self.client = Client()
		self.admin_user = get_user_model().objects.create_superuser(
			email ='kotechashubham94@gmail.com',
			password ='password123'
			)
		self.client.force_login(self.admin_user)

		self.user = get_user_model().objects.create_user(
			email='shubham94@gmail.com',
			password='password123',
			name='Test name'
			)

	def test_users_listed(self):
		"""Tests for listing users"""
		url = reverse('admin:core_customusermodel_changelist')
		res = self.client.get(url)

		self.assertContains(res, self.user.email)



	def test_for_changing_user(self):
		"""Tests for changing user model page works"""
		url = reverse('admin:core_customusermodel_change', args=[self.user.id])
		res = self.client.get(url)

		self.assertEqual(res.status_code, 200)


	def test_for_adding_user(self):
		"""Tests for adding user page works"""
		url = reverse('admin:core_customusermodel_add')
		res = self.client.get(url)

		self.assertEqual(res.status_code, 200)