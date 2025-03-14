# Generated by Django 5.0.3 on 2024-04-17 16:49

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('fam_name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('photo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=30)),
                ('domain_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lesson_id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_description', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterModelOptions(
            name='appuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='appuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='user_id',
        ),
        migrations.AddField(
            model_name='appuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_api.users')),
                ('user_name', models.CharField(max_length=30)),
                ('user_password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_api.users')),
                ('user_type', models.IntegerField()),
                ('grade', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_api.users')),
                ('type_user', models.IntegerField()),
                ('total_XP', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id_task', models.AutoField(primary_key=True, serialize=False)),
                ('XP_pts', models.IntegerField()),
                ('question', models.CharField(max_length=300)),
                ('response', models.CharField(max_length=800)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=300)),
                ('response', models.CharField(max_length=800)),
                ('mark', models.FloatField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('training_id', models.AutoField(primary_key=True, serialize=False)),
                ('training_name', models.CharField(max_length=255)),
                ('training_description', models.CharField(max_length=500)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.domain')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.training'),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id_vid', models.AutoField(primary_key=True, serialize=False)),
                ('XP_pts', models.IntegerField()),
                ('link_vid', models.CharField(max_length=255)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.instructor'),
        ),
        migrations.CreateModel(
            name='IsEnrolled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.learner')),
            ],
            options={
                'unique_together': {('lesson', 'user')},
            },
        ),
    ]
