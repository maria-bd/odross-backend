from django.db import models
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    # Add any additional fields or customization here
    pass

class Domain(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=30)
    domain_description = models.CharField(max_length=255)

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    fam_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=50)
    photo = models.CharField(max_length=50)

class Instructor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    user_type = models.IntegerField()
    grade = models.CharField(max_length=255)

class Learner(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    type_user = models.IntegerField()
    total_XP = models.IntegerField()

class Account(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(max_length=30)
    user_password = models.CharField(max_length=255)

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
    link_vid = models.CharField(max_length=255)

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
