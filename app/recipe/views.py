from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer
from core.models import Tag, Ingredients, recipe


# Create your views here.


class BaseViewsSetAttrs(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	"""Base viewset class"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)


	def get_queryset(self):
		"""Returns objects to current authenticated user only"""
		return self.queryset.filter(user=self.request.user).order_by('-name')


	def perform_create(self, serializer):
		"""Creates and saves it to the authenticated user"""
		serializer.save(user=self.request.user)



class TagViewSet(BaseViewsSetAttrs):
	"""Handles the queryset and serializer"""
	queryset = Tag.objects.all()
	serializer_class = TagSerializer



class IngredientViewSet(BaseViewsSetAttrs):
	"""Handles the queryset and serializer"""
	queryset = Ingredients.objects.all()
	serializer_class = IngredientSerializer



class RecipeViewSet(viewsets.ModelViewSet):
	"""Handles the queryset and serializer"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	serializer_class = RecipeSerializer
	queryset = recipe.objects.all()

	def get_queryset(self):
		"""Returns recipe objects to current authenticated user only"""
		return self.queryset.filter(user=self.request.user).order_by('-id')


	def get_serializer_class(self):
		"""Returns appropriate serializer class"""
		if self.action == 'retrieve':
			return RecipeDetailSerializer

		return self.serializer_class


	def perform_create(self, serializer):
		"""Creates recipe and saves it to the authenticated user"""
		serializer.save(user=self.request.user)