from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

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
    gender = models.CharField(max_length=30, blank=True)  # Added blank=True for optional field
    bio = models.CharField(max_length=500, blank=True)  # Added blank=True for optional field
    photo = models.ImageField(upload_to='images/')  # Added blank=True for optional field
    date_joined = models.DateTimeField(default=timezone.now)
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


class IsEnrolled(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(Learner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('lesson', 'user',)


class Video(models.Model):
    id_vid = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    XP_pts = models.IntegerField()
    link_vid = models.FileField(upload_to='videos/')


class Tasks(models.Model):
    id_task = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    XP_pts = models.IntegerField()
    question = models.CharField(max_length=300)
    response = models.CharField(max_length=800)


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    response = models.CharField(max_length=800)
    mark = models.FloatField()
