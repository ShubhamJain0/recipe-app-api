from user.serializers import CreateUserSerializer, TokenAuthenticating

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Create your views here.


class CreateUser(generics.CreateAPIView):
	"""Handles the serializer"""
	serializer_class = CreateUserSerializer



class TokenGeneration(ObtainAuthToken):
	"""Generates a token to a valid user"""
	serializer_class = TokenAuthenticating
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES