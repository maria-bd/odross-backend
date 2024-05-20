from django.urls import path
from .views import UserRegistration, UserLogin, InstructorLogin, ProfileView, adminLogin, EditProfileView, \
    AppUserCreateAPIView, DomainListView, LessonListView, TrainingListView, VideoCreateAPIView, VideoView, \
    LessonDetailView, ChatBotView, ListCreateQuiz, RetriveUpdateDestroyQuiz, QuizQuestion, QuizQuestionDetail


urlpatterns = [
    path("", ListCreateQuiz.as_view(), name="quiz_list"),
    path("<int:quiz_id>/", RetriveUpdateDestroyQuiz.as_view(), name="quiz_detail"),
    path("questions/<int:quiz_id>/", QuizQuestion.as_view(), name="questions"),
    path("questions/detail/<int:pk>/", QuizQuestionDetail.as_view(), name="question_detail"),
    path('generate/', ChatBotView.as_view(), name='generate_chatbot_response'),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('login2/', InstructorLogin.as_view(), name='instructor-login'),
    path('login3/', adminLogin.as_view(), name='admin-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profileUpdate/', EditProfileView.as_view(), name='profile-update'),
    path('videoPost/', VideoCreateAPIView.as_view(), name='upload_video_api'),
    path('video/', VideoView.as_view(), name='video_api'),
    path('photo/', AppUserCreateAPIView.as_view(), name='upload_photo_api'),
    path('domain/', DomainListView.as_view(), name='domain-list'),
    path('training/', TrainingListView.as_view(), name='training-list'),
    path('lesson/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    # Other URL patterns...
]
