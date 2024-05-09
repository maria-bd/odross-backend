from rest_framework import serializers
from .models import AppUser, Domain, Instructor, Learner, Training, Lesson, IsEnrolled, Video, Tasks, Test
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['name', 'fam_name', 'bio', 'photo']

class adminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                # Check if the user exists and is_staff is True
                user = AppUser.objects.get(email=email, password=password, is_staff=True)
                return user
            except AppUser.DoesNotExist:
                raise ValidationError('User not found')
        else:
            raise ValidationError("Must include 'email' and 'password'.")
class InstructorLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                # Check if the user exists and is_superuser is True
                user = AppUser.objects.get(email=email, password=password, is_superuser=True)
                return user
            except AppUser.DoesNotExist:
                raise ValidationError('User not found or not an instructor')
        else:
            raise ValidationError("Must include 'email' and 'password'.")

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        user = AppUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = AppUser.objects.get(email=email, password=password)
                return user
            except AppUser.DoesNotExist:
                raise ValidationError('User not found')
        else:
            raise ValidationError("Must include 'email' and 'password'.")
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'password', 'email', 'name', 'fam_name', 'gender', 'bio', 'photo', 'date_joined',
                  'is_active', 'is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    total_XP = serializers.IntegerField(source='learner.total_XP', read_only=True)

    class Meta:
        model = AppUser
        fields = ['name', 'fam_name', 'bio', 'photo', 'total_XP']
class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain_id', 'domain_name', 'domain_description']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['user', 'user_type', 'grade']


class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = ['user', 'total_XP']


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['training_id', 'domain', 'training_name', 'training_description']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['lesson_id', 'instructor', 'training', 'lesson_description']


class IsEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsEnrolled
        fields = ['lesson', 'user', 'name']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id_vid', 'lesson', 'XP_pts', 'link_vid']


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id_task', 'lesson', 'XP_pts', 'question', 'response']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['test_id', 'lesson', 'question', 'response', 'mark']
