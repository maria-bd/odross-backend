from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.password = password  # Store password as provided without hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=254)
    name = models.CharField(max_length=255)
    fam_name = models.CharField(max_length=30, blank=True)  # Added blank=True for optional field
    bio = models.CharField(max_length=500, blank=True)  # Added blank=True for optional field
    photo = models.ImageField(upload_to='images/')  # Added blank=True for optional field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Removed 'fam_name', 'gender', 'bio', 'photo' as they are now optional

    def __str__(self):
        return self.email


class Domain(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=30)
    domain_description = models.CharField(max_length=255)


class Instructor(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=255)


class Learner(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    total_XP = models.IntegerField()


class Training(models.Model):
    training_id = models.AutoField(primary_key=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    training_name = models.CharField(max_length=255)
    training_description = models.CharField(max_length=500)


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    lesson_description = models.CharField(max_length=500)


class Video(models.Model):
    id_vid = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    link_vid = models.FileField(upload_to='videos/')
    video_description = models.CharField(max_length=500)
    video_title = models.CharField(max_length=500)


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name=_("Author"))
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    XP_pts = models.IntegerField()
    title = models.CharField(
        _("Quiz Title"), max_length=255, unique=True, default=_("New Quiz")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def question_count(self):
        return self.questions.count()

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ["quiz_id"]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["id"]

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    answer_text = models.CharField(max_length=255, null=True, blank=True)
    is_right = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ["id"]

    def __str__(self):
        return self.answer_text


class IsEnrolled(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(Learner, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user',)

    def __str__(self):
        return f'{self.user} enrolled in {self.quiz}'
