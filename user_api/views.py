from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import AppUser  # Import the AppUser model
from .serializers import UserRegistrationSerializer, ProfileUpdateSerializer, ProfileSerializer, UserLoginSerializer, InstructorLoginSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import VideoSerializer, AppUserSerializer, adminLoginSerializer

class VideoCreateAPIView(APIView):
    permission_classes = [AllowAny]  # Set permission to AllowAny

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppUserCreateAPIView(APIView):
    permission_classes = [AllowAny]  # Set permission to AllowAny

    def post(self, request, format=None):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            name = serializer.validated_data.get('name')
            fam_name = serializer.validated_data.get('fam_name')
            gender = serializer.validated_data.get('gender')
            bio = serializer.validated_data.get('bio')
            photo = request.FILES.get('photo')  # Get the uploaded profile picture

            try:
                user = AppUser.objects.get(email=email)
                user.name = name
                user.fam_name = fam_name
                user.gender = gender
                user.bio = bio
                if photo:
                    user.photo = photo
                user.save()
                return Response({'message': 'Profile updated successfully'})
            except AppUser.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.method == 'GET':
            users = AppUser.objects.all()
            serializer = ProfileSerializer(users, many=True)
            return Response(serializer.data)

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'Login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class adminLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = adminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'amdmin login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InstructorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'Instructor login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(APIView):
    permission_classes = [AllowAny]  # Set the permission class for this view
    def post(self, request):
        if request.method == 'POST':  # Check if the request method is POST
            data = request.data
            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

