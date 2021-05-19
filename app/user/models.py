
from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint,shuffle
from django.shortcuts import reverse
from app.estate_mgt.models import Estate

SEX =[['M','Male'],
      ['F','FeMale']]


def user_id():
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(0,20):
        rand_int = randint(0, 9)
        alpha.append(str(rand_int))
    shuffle(alpha)
    return''.join(alpha[0:20])


def upload_path(instance, filename):
    return instance.get_upload_path(filename)


class RoleManagement(models.Model):
    role_title = models.CharField(max_length=50)

    def __str__(self):
        return self.role_title

    class Meta:
        verbose_name = 'role management'
        verbose_name_plural = 'role management'


class User(AbstractUser):
    user_id = models.CharField(default=user_id, primary_key=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    role = models.ForeignKey(RoleManagement, on_delete=models.CASCADE, related_name='role',blank=True, null=True)
    image = models.ImageField(upload_to=upload_path, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=75, error_messages={'required': "Email Already Exists"})
    notes = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, default="1999-01-01")
    mobile_number = models.BigIntegerField(blank=True, null=True)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, blank=True)
    flat_number = models.CharField( max_length=20, null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    country_short = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=SEX)
    profile_status = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'username': self.username})

    def get_upload_path(self,filename):
        return "estate/{}/users/{}/profile_image/{}".format(self.estate,self.username,filename)

    def save(self, *args, **kwargs):

        if not self.pk:
            try:
                if self.gender == 'M':
                    self.image = 'images/male.png'
                elif self.gender == 'F':
                    self.image = 'images/female.png'
            except:
                pass
        else:
            pass
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user profile'












