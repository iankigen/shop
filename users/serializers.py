from django.core import exceptions
from django.contrib.auth import get_user_model, user_logged_in, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from django.utils.translation import ugettext as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id', 'last_login', 'is_superuser', 'first_name',
			'last_name', 'email', 'date_joined', 'phone_number',
		)
		read_only_fields = ('id', 'last_login', 'is_superuser', 'email', 'date_joined', 'phone_number')


class AuthenticateJWTSerializer(JSONWebTokenSerializer):
	
	def validate(self, attrs):
		credentials = {
			self.username_field: attrs.get(self.username_field),
			'password': attrs.get('password')
		}
		
		if all(credentials.values()):
			user = authenticate(request=self.context['request'], **credentials)
			if user:
				if not user.is_active:
					msg = _('User account is disabled.')
					raise serializers.ValidationError(msg)
				payload = jwt_payload_handler(user)
				user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
				return {
					'token': jwt_encode_handler(payload),
					'user': user
				}
			else:
				msg = _('Unable to log in with provided credentials.')
				raise serializers.ValidationError(msg)
		else:
			msg = _('Must include "{username_field}" and "password".')
			msg = msg.format(username_field=self.username_field)
			raise serializers.ValidationError(msg)


class UserRegistrationSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(User.objects.all())]
	)
	phone_number = serializers.CharField(max_length=13, validators=[UniqueValidator(User.objects.all())])
	password = serializers.CharField(write_only=True)
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	
	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name',
			'email', 'phone_number', 'password'
		)
	
	def validate(self, attrs):
		user = User(**attrs)
		password = attrs.get('password')
		errors = dict()
		try:
			validate_password(password=password, user=user)
		except exceptions.ValidationError as e:
			errors['password'] = list(e.messages)
		if errors:
			raise serializers.ValidationError(errors)
		return super(UserRegistrationSerializer, self).validate(attrs)
	
	def create(self, validated_data):
		user = super(UserRegistrationSerializer, self).create(validated_data)
		user.set_password(validated_data.get('password'))
		user.save()
		return user


class UserPasswordChangerSerializer(serializers.ModelSerializer):
	old_password = serializers.CharField(write_only=True)
	new_password = serializers.CharField(write_only=True)
	
	class Meta:
		model = User
		fields = (
			'old_password', 'new_password',
		)
	
	def validate(self, attrs):
		user = self.context['request'].user
		errors = dict()
		old_password = attrs.get('old_password')
		new_password = attrs.get('new_password')
		
		if not user.check_password(old_password):
			errors['password'] = ['password did not match.']
			raise serializers.ValidationError(errors)
		try:
			validate_password(password=new_password, user=user)
		except exceptions.ValidationError as e:
			errors['password'] = list(e.messages)
		if errors:
			raise serializers.ValidationError(errors)
		return super(UserPasswordChangerSerializer, self).validate(attrs)
	
	def update(self, instance, validated_data):
		instance.set_password(validated_data['new_password'])
		instance.save()
		return instance

		
