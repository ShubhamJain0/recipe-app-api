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



class RecipeSerializer(serializers.ModelSerializer):

	ingredients = serializers.PrimaryKeyRelatedField(
		many=True,
		queryset=models.Ingredients.objects.all()
		)
	tags = serializers.PrimaryKeyRelatedField(
		many=True,
		queryset=models.Tag.objects.all()
		)


	class Meta:
		model = models.recipe
		fields = ('id', 'title', 'time_minutes', 'price', 'link', 'ingredients', 'tags')
		extra_kwargs = {'id':{'read_only':True}}



class RecipeDetailSerializer(RecipeSerializer):

	ingredients = IngredientSerializer(many=True, read_only=True)
	tags = TagSerializer(many=True, read_only=True)