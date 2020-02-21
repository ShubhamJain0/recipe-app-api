import os
import tempfile

from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import recipe, Tag, Ingredients
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


def image_upload_url(recipe_id):
	return 	reverse('recipe:recipe-upload-image', args=[recipe_id])



def detail_url(recipe_id):

	return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tags(user, name='Vegan'):
	"""Creates and returns sample tag"""
	return Tag.objects.create(user=user, name=name)


def sample_ingredients(user, name='Cucumber'):
	"""Creates and returns sample Ingredient"""
	return Ingredients.objects.create(user=user, name=name)

def sample_recipe(user, **params):
	"""Creates and returns sample recipe"""
	defaults = {
	'title':'Sausages',
	'time_minutes':10,
	'price':5.00,
	}

	defaults.update(params)
	return recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):

	def setUp(self):

		self.client = APIClient()


	def test_for_available_to_authenticated_users(self):
		"""Tests that recipe list is available to authenticated users"""
		url = reverse('recipe:recipe-list')
		res = self.client.get(url)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateRecipeApiTest(TestCase):
	"""Test for authenticated users"""

	def setUp(self):

		self.user = get_user_model().objects.create_user(
			email='kotechashubham94@gmail.com',
			password='password1'
			)

		self.client = APIClient()
		self.client.force_authenticate(user=self.user)


	def test_for_retreiving_recipe_list(self):
		"""retreiving recipe list"""
		sample_recipe(user=self.user)
		sample_recipe(user=self.user)

		url = reverse('recipe:recipe-list')
		res = self.client.get(url)

		recipes = recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes, many=True)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)


	def test_for_list_available(self):
		"""Test that recipes are available only for authenticated users"""
		user2 = get_user_model().objects.create_user(
			'kotechshubham94@gmail.com',
			'params1'
			)
		sample_recipe(user=user2)
		sample_recipe(user=self.user)

		url = reverse('recipe:recipe-list')
		res = self.client.get(url)

		recipes = recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data, serializer.data)


	def test_recipe_detail(self):
		"""Test for viewing recipe detail"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tags(user=self.user))
		recipe.ingredients.add(sample_ingredients(user=self.user))

		url = detail_url(recipe.id)
		res = self.client.get(url)

		serializer = RecipeDetailSerializer(recipe)

		self.assertEqual(res.data, serializer.data)


	def test_for_creating_recipe(self):
		"""Test for creating recipe"""
		payload = {
		'title':'Sausages',
		'time_minutes':10,
		'price':5.00,

		}

		url = reverse('recipe:recipe-list')
		res = self.client.post(url, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED	)
		recipes = recipe.objects.get(id=res.data['id'])

		for key in payload.keys():
			self.assertEqual(payload[key], getattr(recipes, key))


	def test_for_creating_recipe_with_tags(self):
		"""Test for creating recipe with tags"""
		tag1 = sample_tags(user=self.user)
		tag2 = sample_tags(user=self.user)
		payload = {
		'title':'Sausages',
		'tags':[tag1.id, tag2.id],
		'time_minutes':10,
		'price':5.00,

		}

		url = reverse('recipe:recipe-list')
		res = self.client.post(url, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		recipes = recipe.objects.get(id=res.data['id'])
		tags = recipes.tags.all()
		self.assertEqual(tags.count(), 2)
		self.assertIn(tag1, tags)
		self.assertIn(tag2, tags)


	def test_for_creating_recipe_with_ingredients(self):
		"""Test for creating recipe with ingredients"""
		ingredient1 = sample_ingredients(user=self.user)
		ingredient2 = sample_ingredients(user=self.user)
		payload = {
		'title':'Sausages',
		'ingredients':[ingredient1.id, ingredient2.id],
		'time_minutes':10,
		'price':5.00,

		}

		url = reverse('recipe:recipe-list')
		res = self.client.post(url, payload)
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		recipes = recipe.objects.get(id=res.data['id'])
		ingredients = recipes.ingredients.all()
		self.assertEqual(ingredients.count(), 2)
		self.assertIn(ingredient1, ingredients)
		self.assertIn(ingredient1, ingredients)


	def test_for_partial_update_recipe(self):
		"""Partially updates the recipe"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tags(user=self.user))
		new_tag = sample_tags(user=self.user, name='Curry')

		payload = {
		'title':'soup',
		'tags':[new_tag.id]
		}

		url = detail_url(recipe.id)
		self.client.patch(url, payload)

		recipe.refresh_from_db()
		self.assertEqual(recipe.title, payload['title'])
		tags = recipe.tags.all()
		self.assertEqual(len(tags), 1)
		self.assertIn(new_tag, tags)


	def test_for_full_update(self):
		"""Fully updates the recipe"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tags(user=self.user))

		payload = {
		'title':'Chicken',
		'time_minutes':14,
		'price':10.00
		}

		url = detail_url(recipe.id)
		self.client.put(url, payload)

		recipe.refresh_from_db()
		self.assertEqual(recipe.title, payload['title'])
		self.assertEqual(recipe.time_minutes, payload['time_minutes'])
		self.assertEqual(recipe.price, payload['price'])



class UploadingImageTest(TestCase):

	def setUp(self):

		self.user = get_user_model().objects.create_user(
			'kotechashubham94@gmail.com',
			'password1'
			)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		self.recipe = sample_recipe(user=self.user)


	def tearDown(self):
		self.recipe.image.delete()


	def test_for_uploading_image_to_recipe(self):
		"""Test for uploading image"""
		url = image_upload_url(self.recipe.id)
		with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
			img = Image.new('RGB', (10, 10))
			img.save(ntf, format='JPEG')
			ntf.seek(0)
			res = self.client.post(url, {'image': ntf}, format='multipart')
		
		self.recipe.refresh_from_db()
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn('image', res.data)
		self.assertTrue(os.path.exists(self.recipe.image.path))


	def test_for_invalid_image(self):
		"""Test uploading an invalid image"""
		url = image_upload_url(self.recipe.id)
		res = self.client.post(url, {'image':'notimage'}, format='multipart')

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


	def test_for_filtering_recipe_with_tags(self):
		"""Tests for filtering recipe with tags"""
		recipe1 = sample_recipe(user=self.user, title='Sausages')
		recipe2 = sample_recipe(user=self.user, title='Curry')
		tag1 = sample_tags(user=self.user, name='Non-Veg')
		tag2 = sample_tags(user=self.user, name='Vegan')
		recipe1.tags.add(tag1)
		recipe2.tags.add(tag2)
		recipe3 = sample_recipe(user=self.user, title='Soup')

		url = reverse('recipe:recipe-list')
		res = self.client.get(url, {'tags':f'{tag1.id},{tag2.id}'})

		serializer1 = RecipeSerializer(recipe1)
		serializer2 = RecipeSerializer(recipe2)
		serializer3 = RecipeSerializer(recipe3)

		self.assertIn(serializer1.data, res.data)
		self.assertIn(serializer2.data, res.data)
		self.assertNotIn(serializer3.data, res.data)


	def test_for_filtering_recipes_with_ingredients(self):
		"""Tests for filtering recipes with ingredients"""
		recipe1 = sample_recipe(user=self.user, title='Sausages')
		recipe2 = sample_recipe(user=self.user, title='Curry')
		ingredient1 = sample_ingredients(user=self.user, name='Sausage')
		ingredient2 = sample_ingredients(user=self.user, name='Carrot')
		recipe1.ingredients.add(ingredient1)
		recipe2.ingredients.add(ingredient2)
		recipe3 = sample_recipe(user=self.user, title='Soup')

		url = reverse('recipe:recipe-list')
		res = self.client.get(url, {'ingredients':f'{ingredient1.id},{ingredient2.id}'})

		serializer1 = RecipeSerializer(recipe1)
		serializer2 = RecipeSerializer(recipe2)
		serializer3 = RecipeSerializer(recipe3)

		self.assertIn(serializer1.data, res.data)
		self.assertIn(serializer2.data, res.data)
		self.assertNotIn(serializer3.data, res.data)