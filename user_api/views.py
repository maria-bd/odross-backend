from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import AppUser, Domain, Lesson, Training, Video
from .serializers import UserRegistrationSerializer, ProfileSerializer, UserLoginSerializer, InstructorLoginSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import VideoSerializer, AppUserSerializer, adminLoginSerializer, LearnerSerializer, \
    EditProfileSerializer, DomainSerializer, LessonSerializer, TrainingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import generate_mock_response  # Assuming utils.py is in the same directory
from .chatbot import ChatBot
from configparser import ConfigParser
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.views import APIView
from django.http import Http404


class ListCreateQuiz(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class RetriveUpdateDestroyQuiz(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_url_kwarg = "quiz_id"


class QuizQuestion(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format="None", **kwargs):
        question = Question.objects.filter(quiz_id=kwargs["quiz_id"])
        serializer = QuestionSerializer(question, many=True)

        return Response(serializer.data)

    def post(self, request, format=None, **kwargs):
        quiz = Quiz.objects.get(id=kwargs["quiz_id"])
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(quiz=quiz)
            return Response(
                {"message": "Question created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )


class QuizQuestionDetail(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Question.objects.get(id=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(
            {"message": "Question deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
class ChatBotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_input = request.data.get('message', '')
            if not user_input:
                return Response({'error': 'No message provided'}, status=400)

            config = ConfigParser()
            config.read('credentials.ini')
            api_key = config['gemini_ai']['API_KEY']

            chatbot = ChatBot(api_key=api_key)
            response = chatbot.ChatWithModel(user_input)
            return Response({'response': response})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
class VideoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lesson = request.GET.get('lesson', None)
        if lesson:
            try:
                videos = Video.objects.filter(lesson=lesson)
                serializer = VideoSerializer(videos, many=True)
                return Response(serializer.data)
            except Video.DoesNotExist:
                return Response({"error": "Videos not found for this lesson"}, status=404)
        else:
            return Response({"error": "lesson_id parameter is required"}, status=400)
class DomainListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Check if the HTTP method is GET
        if request.method == 'GET':
            # Retrieve all domain objects
            domains = Domain.objects.all()
            # Serialize the data
            serializer = DomainSerializer(domains, many=True)
            # Return the serialized data
            return Response(serializer.data)

class TrainingListView(APIView):
        permission_classes = [AllowAny]
        def get(self, request):
            if request.method == 'GET':
               trainings = Training.objects.all()
                # Serialize the data
               serializer = TrainingSerializer(trainings, many=True)
               return Response(serializer.data)
class LessonDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, lesson_id):
        try:
            # Retrieve the lesson object based on the provided lesson_id
            lesson = Lesson.objects.get(lesson_id=lesson_id)
            # Serialize the lesson data along with the associated videos
            serializer = LessonSerializer(lesson)
            serialized_data = serializer.data

            # Fetch and serialize the videos associated with the lesson
            videos = Video.objects.filter(lesson=lesson)
            video_serializer = VideoSerializer(videos, many=True)
            serialized_data['videos'] = video_serializer.data

            # Return the updated serialized data
            return Response(serialized_data)
        except Lesson.DoesNotExist:
            # Return a 404 Not Found response if the lesson does not exist
            return Response(status=status.HTTP_404_NOT_FOUND)
class LessonListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Check if the HTTP method is GET
        if request.method == 'GET':
            # Retrieve all domain objects
            Lessons = Lesson.objects.all()
            # Serialize the data
            serializer = LessonSerializer(Lessons, many=True)
            # Return the serialized data
            return Response(serializer.data)
class EditProfileView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"error": "Email parameter is required"}, status=400)

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = EditProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
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
        email = request.GET.get('email', None)
        if email:
            try:
                user = AppUser.objects.get(email=email)
                serializer = ProfileSerializer(user)
                return Response(serializer.data)
            except AppUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            return Response({"error": "Email parameter is required"}, status=400)
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

