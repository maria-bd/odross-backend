from .models import AppUser, Domain, Instructor, Learner, Training, Lesson, IsEnrolled, Video
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Quiz, Question, Answer, AppUser
from django.contrib.auth import get_user_model, authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def create(self, validated_data):
        user_password = validated_data.get('password', None)
        db_instance = self.Meta.model(email=validated_data.get('email'))
        db_instance.set_password(user_password)
        db_instance.save()
        return db_instance

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
    token = serializers.CharField(max_length=255, read_only=True)

class QuizSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            "quiz_id",
            "title",
            "created_at",
            "question_count",
            "XP_pts"
        ]

    def get_question_count(self, obj):
        return obj.question_count


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "id",
            "answer_text",
            "is_right"
        ]


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "quiz",
            "title",
            "answers",
        ]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        question = Question.objects.create(**validated_data)

        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        # Update the associated answers
        answers_data = validated_data.pop("answers", [])
        instance.answers.all().delete()  # Deleting existing answers
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)

        return instance


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['name', 'fam_name', 'password', 'photo', 'bio']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.fam_name = validated_data.get('fam_name', instance.fam_name)
        instance.password = validated_data.get('password', instance.password)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
'''
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
class InstructorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        user = AppUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            is_superuser=True
        )
        return user
'''''
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'password', 'email', 'name', 'fam_name', 'bio', 'photo', 'is_active', 'is_staff']


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
    quiz = QuizSerializer()
    user = LearnerSerializer()

    class Meta:
        model = IsEnrolled
        fields = ['id', 'quiz', 'user', 'enrollment_date']

class VideoSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    class Meta:
        model = Video
        fields = ['id_vid', 'lesson', 'link_vid', 'video_description', 'video_title']
