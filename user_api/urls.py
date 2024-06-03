from django.urls import path
from .views import AppUserCreateAPIView, DomainListView, LessonListView, TrainingListView, VideoCreateAPIView, \
    VideoView, LessonDetailView, ChatBotView, ListQuiz, RetriveUpdateDestroyQuiz, QuizQuestion, QuizQuestionDetail, \
    CreateQuiz, TopUsersView, AppUserListView, StatisticsView, InstructorRegistration, UserRegistrationAPIView, \
    UserLoginAPIView, UserViewAPI, UserLogoutViewAPI, AppUserView, DomainDetailView
from . import views

urlpatterns = [
    # user login stuff
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutViewAPI.as_view(), name='logout'),
    path('user/', UserViewAPI.as_view(), name='user'),
    # stuff that works lol
    path('stat/', StatisticsView.as_view(), name='statistics'),
    path('top-users/', TopUsersView.as_view(), name='top-users'),
    path("", ListQuiz.as_view(), name="quiz_list"),
    path("create_quiz/", CreateQuiz.as_view(), name="create_quiz"),
    path("<int:quiz_id>/", RetriveUpdateDestroyQuiz.as_view(), name="quiz_detail"),
    path("questions/<int:quiz_id>/", QuizQuestion.as_view(), name="questions"),
    path("questions/detail/<int:pk>/", QuizQuestionDetail.as_view(), name="question_detail"),
    path('generate/', ChatBotView.as_view(), name='generate_chatbot_response'),
    # path('1register/', UserRegistration.as_view(), name='user-registration'),
    # path('1login/', UserLogin.as_view(), name='user_login'),
    # path('login2/', InstructorLogin.as_view(), name='instructor-login'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profileUpdate/', EditProfileView.as_view(), name='profile-update'),
    path('videoPost/', VideoCreateAPIView.as_view(), name='upload_video_api'),
    path('video/', VideoView.as_view(), name='video_api'),
    path('photo/', AppUserCreateAPIView.as_view(), name='upload_photo_api'),
    path('domain/', DomainListView.as_view(), name='domain-list'),
    path('domain/<int:pk>/', DomainDetailView.as_view(), name='domain-detail'),
    path('training/', TrainingListView.as_view(), name='training-list'),
    path('lesson/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    # admin stuff
    path('admin/learner/', AppUserListView.as_view(), name='learner-list'),
    path('admin/learner/<int:pk>/', AppUserListView.as_view(), name='app_user_detail'),
    path('admin/learner/1/<int:pk>/', AppUserView.as_view(), name='app_user_one'),
    path('admin/instructor/', InstructorRegistration.as_view(), name='instructor-register'),
    # path('login3/', adminLogin.as_view(), name='admin-login'),
]
