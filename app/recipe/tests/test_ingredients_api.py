from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import  Ingredients, recipe
from recipe.serializers import IngredientSerializer




class PublicApiIngredientTest(TestCase):

	def setUp(self):

		self.client = APIClient()


	def test_for_authenticated_user(self):
		"""Tests that Ingredient list is available to authenticated users"""
		url = reverse('recipe:ingredients-list')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiIngredientTest(TestCase):
	"""Test for authenticated users"""

	def setUp(self):

		self.user = get_user_model().objects.create_user(
			email='kotechashubham94@gmail.com',
			password='password'
			)

		self.client = APIClient()
		self.client.force_authenticate(user=self.user)


	def test_for_retrieving_ingredient_list(self):
		"""retrieves ingredient list"""
		Ingredients.objects.create(user=self.user, name='Cucumber')
		Ingredients.objects.create(user=self.user, name='Potato')

		url = reverse('recipe:ingredients-list')
		res = self.client.get(url)

		ingredients = Ingredients.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredients, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)


	def test_for_ingredient_list_available(self):
		"""Test that ingredients are available only for authenticated users"""
		user2 = get_user_model().objects.create_user(
			email='kotecshubham94@gmail.com',
			password='password'
			)

		Ingredients.objects.create(user=user2, name='Cabbage')
		ingredients =  Ingredients.objects.create(user=self.user, name='Chilli')

		url = reverse('recipe:ingredients-list')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], ingredients.name)


	def test_for_ingredients_create(self):
		"""Test for creating ingredients"""
		payload = {'name':'Chilli'}

		url = reverse('recipe:ingredients-list')
		res = self.client.post(url, payload)

		exists = Ingredients.objects.filter(
			user=self.user,
			name='Chilli'
			).exists()
		self.assertTrue(exists)


	def test_for_invalid_ingredient(self):
		"""Test for invalid ingredient"""
		payload = {'name':''}

		url = reverse('recipe:ingredients-list')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_retrieving_assigned_ingredients(self):
		"""Tests that only the ingredients that are assigned to recipe are retrieved"""
		ingredient1 = Ingredients.objects.create(
			user=self.user,
			name='Chilli'
			)
		ingredient2 = Ingredients.objects.create(
			user=self.user,
			name='Cabbage'
			)
		recipes = recipe.objects.create(
			user=self.user,
			title='Toast',
			time_minutes=10,
			price=2.00
			)
		recipes.ingredients.add(ingredient1)

		url = reverse('recipe:ingredients-list')
		res = self.client.get(url, {'assigned_only':1})

		serializer1 = IngredientSerializer(ingredient1)
		serializer2 = IngredientSerializer(ingredient2)

		self.assertIn(serializer1.data, res.data)
		self.assertNotIn(serializer2.data, res.data)