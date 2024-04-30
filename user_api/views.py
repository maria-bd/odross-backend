from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # Import the permission class you want to use
from .serializers import UserRegistrationSerializer, UserLoginSerializer

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

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'Login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
