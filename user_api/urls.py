from django.urls import path
from .views import UserRegistration, UserLogin, InstructorLogin

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('login2/', InstructorLogin.as_view(), name='instructor-login'),
    # Other URL patterns...
]
