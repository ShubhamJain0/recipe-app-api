from user.serializers import UserSerializer, TokenAuthenticating

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Create your views here.


class CreateUser(generics.CreateAPIView):
	"""Handles the serializer"""
	serializer_class = UserSerializer



class TokenGeneration(ObtainAuthToken):
	"""Generates a token to a valid user"""
	serializer_class = TokenAuthenticating
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class ManagingUser(generics.RetrieveUpdateAPIView):
	"""Retrieves and updates the authenticated user profile"""
	serializer_class = UserSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		"""Retrieves the authenticated user"""
		return self.request.user