from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):

	class Meta:

		model = models.Tag
		fields = ('id', 'name')
		read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Ingredients
		fields = ('id', 'name')
		extra_kwargs = {'id':{'read_only':True}}