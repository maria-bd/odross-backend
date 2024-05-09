from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import AppUser  # Import the AppUser model
from .serializers import UserRegistrationSerializer, ProfileSerializer, UserLoginSerializer, InstructorLoginSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import VideoSerializer, AppUserSerializer, adminLoginSerializer, LearnerSerializer

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
    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == 'POST':
            data = request.data
            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()  # Save the user instance
                # Create a Learner instance associated with the user
                learner_data = {'user': user.id, 'total_XP': 0}  # Assuming total_XP starts from 0
                learner_serializer = LearnerSerializer(data=learner_data)
                if learner_serializer.is_valid():
                    learner_serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    user.delete()  # Rollback user creation if learner creation fails
                    return Response(learner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

