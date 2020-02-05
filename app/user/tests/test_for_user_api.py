from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status



class PublicUserApiTest(TestCase):


	def setUp(self):
		self.client = APIClient()


	def test_for_user_created(self):
		"""Test for creating user with valid payload"""
		payload = {
		'email':'kotechashubham94@gmail.com',
		'password':'pass123',
		'name':'ok'
		}

		url = reverse('user:create')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password', res.data)


	def test_for_user_exist(self):
		"""Test for user if it exists"""
		payload = {
		'email':'kotechashubham94@gmail.com',
		'password':'payload1',
		'name':'name1'
		}

		user = get_user_model().objects.create_user(**payload)

		url = reverse('user:create')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_for_password_length(self):
		"""Test for password min length"""
		payload = {
		'email':'kotechashubham94@gmail.com',
		'password':'pwe',
		'name':'na'
		}

		url = reverse('user:create')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email=payload['email']
			).exists()
		self.assertFalse(user_exists)


	def test_for_token_user(self):
		"""Test that a token is created for a valid user"""
		payload = {'email':'kotechashubham94@gmail.com', 'password':'password1'}
		user = get_user_model().objects.create_user(**payload)

		url = reverse('user:token')
		res = self.client.post(url, payload)

		self.assertIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)


	def test_for_invalid_user(self):
		"""Tests for the user's invalid credentials"""
		payload = {'email':'kotechashubham94@gmail.com', 'password':'password1'}
		user = get_user_model().objects.create_user(
			email='kotechashubham94@gmail.com',
			password='password3'
			)

		url = reverse('user:token')
		res = self.client.post(url, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_for_no_user(self):
		"""Test that no token is created if user doesn't exist"""
		payload = {'email':'kotechashubham94@gmail.com', 'password':'password1'}

		url = reverse('user:token')
		res = self.client.post(url, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_for_missing_field_data(self):
		"""Test that no token is created if there is a missing field data"""
		payload = {'email':'kotechashubham94@gmail.com', 'password':''}
		user = get_user_model().objects.create_user(**payload)

		url = reverse('user:token')
		res = self.client.post(url, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_for_authentication_required(self):
		"""Test that authentication is required for users for updating profiles"""
		url = reverse('user:me')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateUserApiTest(TestCase):

	def setUp(self):

		self.user = get_user_model().objects.create_user(
			email='kotechashubham94@gmail.com',
			password='payload1',
			name='name'
			)
		self.client = APIClient()

		self.client.force_authenticate(user=self.user)


	def test_for_retreiving_profile(self):
		"""Test for retreiving profile of logged in user"""
		url = reverse('user:me')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, {
			'email':self.user.email,
			'name':self.user.name
			})


	def test_for_no_post_is_allowed(self):
		"""Test that post request is not allowed on me url """
		url = reverse('user:me')
		res = self.client.post(url, {})

		self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


	def test_for_updating_authenticated_user_profile(self):
		"""Test for updating authenticated user profile"""
		payload = {'name':'name1', 'password':'password123'}

		url = reverse('user:me')
		res = self.client.patch(url, payload)

		self.user.refresh_from_db()
		self.assertEqual(self.user.name, payload['name'])
		self.assertTrue(self.user.check_password(payload['password']))
		self.assertEqual(res.status_code, status.HTTP_200_OK)