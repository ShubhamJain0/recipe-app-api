from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Ingredients
from recipe.serializers import TagSerializer, IngredientSerializer



class PublicUserTagTest(TestCase):

	def setUp(self):

		self.client = APIClient()

	def test_for_authenticated_users(self):
		"""Tests that tags list is available only to authenticated users"""
		url = reverse('recipe:tag-list')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTagTest(TestCase):
	"""Test for authenticated users"""

	def setUp(self):

		self.user = get_user_model().objects.create_user(
			email='kotechashubham94@gmail.com',
			password='password123'
			)

		self.client = APIClient()

		self.client.force_authenticate(user=self.user)


	def test_for_tag_list(self):
		"""Test for retreiving tags list"""
		Tag.objects.create(user=self.user, name='Vegan')
		Tag.objects.create(user=self.user, name='Dessert')

		url = reverse('recipe:tag-list')
		res = self.client.get(url)

		tags = Tag.objects.all().order_by('-name')
		serializer = TagSerializer(tags, many=True)

		

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)


	def test_for_tag_available(self):
		"""Test that tags are available only for authenticated users"""
		user2 = get_user_model().objects.create_user(
			email='shubham@gmail.com',
			password='password'
			)
		Tag.objects.create(user=user2, name='Meat')
		tag = Tag.objects.create(user=self.user, name='Fruit')

		url = reverse('recipe:tag-list')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], tag.name)


	def test_for_creating_tags(self):
		"""Test for creating tags"""
		payload = {'name':'veg'}

		url = reverse('recipe:tag-list')
		res = self.client.post(url, payload)

		exists = Tag.objects.filter(
			user=self.user,
			name='veg'
			).exists()
		self.assertTrue(exists)


	def test_for_invalid_tag(self):
		"""Test for invalid tag"""
		payload = {'name':''}

		url = reverse('recipe:tag-list')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




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