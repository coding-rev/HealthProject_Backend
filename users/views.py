from django.shortcuts import render
from .models import * 
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, logout
from django.contrib import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
# Create your views here.

class RegistrationView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		data = UserSerializer(data=request.data)
		data.is_valid(raise_exception=True)
		validated_data = data.data
		email = validated_data["email"]
		
		if User.objects.filter(email=email).exists():
			return Response({
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"message": "Email already exist"
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			try:
				getPassword = request.data["password"]
				password_length = len(getPassword)
				if "@" not in email and ".com" not in email:
					return Response({
						"status": status.HTTP_400_BAD_REQUEST,
						"message": "Invalid email input",
					}, status=status.HTTP_400_BAD_REQUEST)
				elif password_length < 8:
					return Response({
						"status": status.HTTP_400_BAD_REQUEST,
						"message": "Password must contain at least 8 characters",
					}, status=status.HTTP_400_BAD_REQUEST)
				else:
					
					user = User.objects.create(
							full_name=validated_data["full_name"],
							email=email
						)
					user.set_password(getPassword)
					user.userId = generate_userId()
					user.is_patient = validated_data['is_patient']
					user.is_doctor = validated_data['is_doctor']
					user.save()
										
					return Response({
						"status": status.HTTP_201_CREATED,
						"email": user.email,
						"message": "Account registration is successful."
						
					}, status=status.HTTP_201_CREATED)
					

			except Exception as e:
				return Response({
					"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
					"message": "Something went wrong. " + str(e),
				}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(GenericAPIView):
	serializer_class = UserLoginSerializer
	permission_classes = [AllowAny]

	def post(self, request):
		data = UserLoginSerializer(data=request.data)
		data.is_valid(raise_exception=True)
		validated_data = data.data 

		email = validated_data["email"]
		password = validated_data["password"]
		user = auth.authenticate(email=email, password=password)
		if user:
			token = RefreshToken.for_user(user).access_token
			serializer = UserLoginSerializer(user)
			print("LOGIN SUCCESFUL")
			data = {
				'status': status.HTTP_200_OK,
				'userId': user.userId,
				'token': str(token),
			}
			return Response(data, status=status.HTTP_200_OK)
			
		return Response({
			'status': status.HTTP_404_NOT_FOUND,
			'message': 'Please enter the correct username and password. Note that both fields may be case-sensitive'
		}, status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		logout(request)
		return Response({
			"status":status.HTTP_200_OK,
			"message":"Logged out"
			}, status=status.HTTP_200_OK)

#Doctor Views
class GetAllDoctorsView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserListSerializer

	def get(self, request):
		allDoctors = User.objects.filter(is_doctor=True).order_by("-pk")
		data = UserListSerializer(allDoctors, many=True)
		return Response({
			"status": status.HTTP_200_OK,
			"data": data.data
			}, status=status.HTTP_200_OK)

# Patient Views
class GetAllPatientsView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserListSerializer

	def get(self, request):
		allPatients = User.objects.filter(is_patient=True).order_by("-pk")
		data = UserListSerializer(allPatients, many=True)
		return Response({
			"status": status.HTTP_200_OK,
			"data": data.data
			}, status=status.HTTP_200_OK)


class EditProfilePicView(APIView):
	permission_classes 	= [AllowAny]
	serializer_class 	= ProfilePictureSerializer

	def put(self, request, id, format=None):
		data 	=	ProfilePictureSerializer(data=request.data)
		data.is_valid(raise_exception=True)

		try:
			user = User.objects.get(id=id)
			user.profile_image = request.FILES["profile_image"]
			user.save()
			return Response({
				"status": status.HTTP_200_OK,
				"message": "Profile picture updated successfully"
			}, status=status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({
				"status": status.HTTP_400_BAD_REQUEST,
				"message": "User does not exist"
			}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"message": str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditUser(APIView):
	permission_classes 	= [AllowAny]
	serializer_class 	= EditUserSerializer 

	def put(self, request, id):
		data 		= EditUserSerializer(data=request.data)
		data.is_valid(raise_exception=False)
		validated_data = data.data

		try:
			user 			= User.objects.get(id=id)
			user.full_name 	= validated_data["full_name"]
			user.email 		= validated_data["email"]
			user.phone 		= validated_data["phone"]
			user.save()

			return Response({
				"status":status.HTTP_200_OK,
				"message":"Profile updated successfully"
				}, status=status.HTTP_200_OK)

		except Exception as e:
			return Response({
				"status":status.HTTP_400_BAD_REQUEST,
				"message":str(e)
				}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		try:
			user 		= User.objects.get(id=id)
			user.delete()
			return Response({
				"status":status.HTTP_200_OK,
				"message":"User deleted successfully"
				}, status=status.HTTP_200_OK)
		except:
			return Response({
				"status":status.HTTP_404_NOT_FOUND,
				"message":"User not found"
				}, status=status.HTTP_404_NOT_FOUND)