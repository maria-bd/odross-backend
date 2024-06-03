from .models import AppUser, Domain, Lesson, Training, Video, Instructor, Learner, IsEnrolled
from .serializers import ProfileSerializer
# InstructorLoginSerializer
from .serializers import VideoSerializer, AppUserSerializer, LearnerSerializer, EditProfileSerializer,\
    DomainSerializer, LessonSerializer, TrainingSerializer
from .chatbot import ChatBot
from configparser import ConfigParser
from rest_framework import generics, status
from .models import Quiz, Question, Answer
from .serializers import QuizSerializer, QuestionSerializer
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import generate_access_token
import jwt


class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Hello!'}
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            if new_user:
                access_token = generate_access_token(new_user)
                data = {'access_token': access_token}
                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)

                # Adding learner creation functionality
                learner_data = {'user': new_user.id, 'total_XP': 0}
                learner_serializer = LearnerSerializer(data=learner_data)
                if learner_serializer.is_valid():
                    learner_serializer.save()
                    return response
                else:
                    new_user.delete()  # Rollback user creation if learner creation fails
                    return Response(learner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', None)
        user_password = request.data.get('password', None)

        if not user_password:
            raise AuthenticationFailed('A user password is needed.')

        if not email:
            raise AuthenticationFailed('An user email is needed.')

        user_instance = authenticate(username=email, password=user_password)

        if not user_instance:
            raise AuthenticationFailed('User not found.')

        if user_instance.is_active:
            user_access_token = generate_access_token(user_instance)
            response = Response()
            response.set_cookie(key='access_token', value=user_access_token, httponly=True)
            response.data = {'access_token': user_access_token}
            return response

        return Response({'message': 'Something went wrong.'})

'''class UserViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(id=payload['id']).first()
        user_serializer = UserRegistrationSerializer(user)
        return Response(user_serializer.data)'''
class UserViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(id=payload['id']).first()

        if not user:
            raise AuthenticationFailed('User not found.')

        profile_serializer = ProfileSerializer(user)
        return Response(profile_serializer.data)

class UserLogoutViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token', None)
        if user_token:
            response = Response()
            response.delete_cookie('access_token')
            response.data = {
                'message': 'Logged out successfully.'
            }
            return response
        response = Response()
        response.data = {
            'message': 'User is already logged out.'
        }
        return response

# User stuff
'''
class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
'''
# quiz 1.0
class CreateQuiz(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error message

class ListQuiz(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DomainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DomainDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Domain.objects.get(pk=pk)
        except Domain.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        domain = self.get_object(pk)
        serializer = DomainSerializer(domain)
        return Response(serializer.data)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            try:
                domain = Domain.objects.get(pk=pk)
                domain.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Domain.DoesNotExist:
                return Response({"error": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class TopUsersView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        top_users = AppUser.objects.filter(learner__isnull=False).order_by('-learner__total_XP')[:10]
        serializer = ProfileSerializer(top_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        # Retrieve the authenticated user's profile or return 404 if not found
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
'''
# instructor stuff
class InstructorLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InstructorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'Instructor login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
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
'''
# Admin stuff
class StatisticsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.method == 'GET':
           stats = {
            'app_user_count': AppUser.objects.count(),
            'domain_count': Domain.objects.count(),
            'instructor_count': Instructor.objects.count(),
            'learner_count': Learner.objects.count(),
            'training_count': Training.objects.count(),
            'lesson_count': Lesson.objects.count(),
            'video_count': Video.objects.count(),
            'quiz_count': Quiz.objects.count(),
            'question_count': Question.objects.count(),
            'answer_count': Answer.objects.count(),
            'is_enrolled_count': IsEnrolled.objects.count(),
           }
           return Response(stats)
class adminLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = adminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # You can customize the response as per your requirement
            return Response({'message': 'amdmin login successful', 'name': user.name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if request.method == 'GET':
            app_user = AppUser.objects.get(pk=pk)
            app_users = AppUser.objects.filter(is_superuser=False, is_staff=False)
            serializer = AppUserSerializer(app_users, many=True)

            # Append image URLs to each user
            for user_data in serializer.data:
                user_data['photo_url'] = request.build_absolute_uri(user_data['photo'])

            return Response(serializer.data)

class AppUserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.method == 'GET':
            app_users = AppUser.objects.filter(is_superuser=False, is_staff=False)
            serializer = AppUserSerializer(app_users, many=True)

            # Append image URLs to each user
            for user_data in serializer.data:
                user_data['photo_url'] = request.build_absolute_uri(user_data['photo'])

            return Response(serializer.data)

    def put(self, request, pk):
        if request.method == 'PUT':
            app_user = AppUser.objects.get(pk=pk)
            serializer = AppUserSerializer(app_user, data=request.data, partial=True)  # Specify partial=True
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.method == 'DELETE':
            try:
                app_user = AppUser.objects.get(pk=pk)
                app_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except AppUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InstructorRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == 'POST':
            data = request.data
            serializer = InstructorRegistrationSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()  # Save the user instance with is_superuser=True
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