from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers




class CreateUserSerializer(serializers.ModelSerializer):
	"""Takes in the user input"""

	class Meta:
		model = get_user_model()
		fields = ('email', 'password', 'name')
		extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

	def create(self, validated_data):
		"""Creates an object"""
		return get_user_model().objects.create_user(**validated_data)



class TokenAuthenticating(serializers.Serializer):

	email = serializers.CharField()
	password = serializers.CharField(
		style = {'input_type':'password'},
		trim_whitespace = False
		)


	def validate(self, attrs):
		"""Validates the data"""
		email = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(
			request=self.context.get('request'),
			username=email,
			password=password
			)
		if not user:
			msg = _('Provided credentials are not valid, no token is generated!')
			raise serializers.ValidationError(msg, code='authentication')

		attrs['user'] = user
		return attrs