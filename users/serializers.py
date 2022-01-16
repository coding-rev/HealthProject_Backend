from rest_framework import serializers
from .import models 

class UserSerializer(serializers.ModelSerializer):
	full_name = serializers.CharField(max_length=200)
	password = serializers.CharField(
		max_length=65, min_length=8, write_only=True)
	email = serializers.EmailField(max_length=255, min_length=4)
	is_doctor = serializers.BooleanField()
	is_patient = serializers.BooleanField()
	class Meta:
		model= models.User
		fields = ['full_name', 'email', 'is_patient','is_doctor','password']
		extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=65, min_length=8)
	email = serializers.EmailField(max_length=255, min_length=4)

	class Meta:
		model = models.User
		fields = ["email", "password"]

class UserListSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.User 
		exclude = ['password', 'username']