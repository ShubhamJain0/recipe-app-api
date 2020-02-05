from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredients


# Create your views here.


class BaseViewsSetAttrs(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	"""Base viewset class"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)


	def get_queryset(self):
		"""Returns tag objects to current authenticated user only"""
		return self.queryset.filter(user=self.request.user).order_by('-name')


	def perform_create(self, serializer):
		"""Creates tag and saves it to the authenticated user"""
		serializer.save(user=self.request.user)



class TagViewSet(BaseViewsSetAttrs):
	"""Handles the queryset and serializer"""
	queryset = Tag.objects.all()
	serializer_class = TagSerializer



class IngredientViewSet(BaseViewsSetAttrs):
	"""Handles the queryset and serializer"""
	queryset = Ingredients.objects.all()
	serializer_class = IngredientSerializer
