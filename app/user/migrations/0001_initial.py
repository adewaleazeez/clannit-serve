# Generated by Django 2.0.4 on 2018-05-16 14:31

import app.user.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('estate_mgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(default=app.user.models.user_id, max_length=30, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to=app.user.models.upload_path)),
                ('email', models.EmailField(error_messages={'required': 'Email Already Exists'}, max_length=75, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('date_of_birth', models.DateField(blank=True, default='1999-01-01')),
                ('mobile_number', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('flat_number', models.CharField(blank=True, max_length=20, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('country_short', models.CharField(blank=True, max_length=15, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(choices=[['M', 'Male'], ['F', 'FeMale']], max_length=1)),
                ('estate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='estate_mgt.Estate')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user profile',
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RoleManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'role management',
                'verbose_name_plural': 'role management',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='user.RoleManagement'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
