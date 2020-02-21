import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.


def recipe_image_file_path(instance, filename):
	"""Genrates the recipe image path"""
	ext = filename.split('.')[-1]
	filename = f'{uuid.uuid4()}.{ext}'

	return os.path.join('uploads/recipe/', filename)



class CustomUserModelManager(BaseUserManager):

	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('Email is needed!')

		email=self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):

		user=self.create_user(email, password)

		user.is_superuser=True
		user.is_staff=True
		user.save(using=self._db)

		return user






class CustomUserModel(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(unique=True, max_length=255)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = CustomUserModelManager()

	USERNAME_FIELD = 'email'



class Tag(models.Model):

	name = models.CharField(max_length=255)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		)

	def __str__(self):
		"""Returns the string representation"""
		return self.name



class Ingredients(models.Model):

	name = models.CharField(max_length=255)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)

	def __str__(self):
		"""Returns the string representation"""
		return self.name



class recipe(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	title = models.CharField(max_length=255)
	time_minutes = models.IntegerField()
	price = models.DecimalField(max_digits=5, decimal_places=2)
	link = models.CharField(blank=True, max_length=255)
	ingredients = models.ManyToManyField('Ingredients')
	tags = models.ManyToManyField('Tag')
	image = models.ImageField(null=True, upload_to=recipe_image_file_path)


	def __str__(self):
		"""Returns the string representation"""
		return self.title