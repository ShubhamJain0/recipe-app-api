from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.



class CustomUserModelManager(BaseUserManager):

	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Email is needed!')

		email=self.normalize_email(email)
		user = self.model(email=email)
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