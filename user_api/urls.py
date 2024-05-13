from django.urls import path
from .views import UserRegistration, UserLogin, InstructorLogin, ProfileView, adminLogin, EditProfileView, \
    AppUserCreateAPIView, DomainListView, LessonListView, TrainingListView, VideoCreateAPIView, VideoView, \
    LessonDetailView

urlpatterns = [
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
