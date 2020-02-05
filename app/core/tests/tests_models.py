from django.test import TestCase
from  django.contrib.auth import get_user_model

from core.models import Tag, Ingredients


class ModelTest(TestCase):

	def test_for_email_password(self):
		"""Checks for the email and password"""
		email='kotechashubham94@gmail.com'
		password='password123'
		user=get_user_model().objects.create_user(
			email=email,
			password=password
			
			)
		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))



	def test_normalizing(self):
		"""Normalizes the email"""
		email='kotechashubham94@Gmail.com'
		password='password123'
		user=get_user_model().objects.create_user(

			email=email,
			password=password
			)

		self.assertEqual(user.email, email.lower())

	def test_for_email_validation(self):
		"""Raises a value error"""
		password='password123'
		with self.assertRaises(ValueError):
			user=get_user_model().objects.create_user(None, password=password)

	def test_for_superusers(self):
		"""Tests for the superuser status"""
		user=get_user_model().objects.create_superuser('kotechashubham94@gmail.com', 'password123')

		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)


	def test_for_tag_model(self):
		"""Test for Tag string representation"""
		tag = Tag.objects.create(
			user=get_user_model().objects.create_user(
				email='kotechashubham94@gmail.com',
				password='password1'
				),
			name='Vegan'
			)

		self.assertEqual(str(tag), tag.name)


	def test_for_ingredients_model(self):
		"""Test for ingredient string representation"""
		ingredient = Ingredients.objects.create(
			user=get_user_model().objects.create_user(
				email='kotechashubham94@gmail.com',
				password='password1'
				),
			name='Carrot'
			)

		self.assertEqual(str(ingredient), ingredient.name)