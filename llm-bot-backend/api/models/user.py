from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
import uuid


def get_profile_image_path(self, filename):
    return f'profile_images/users/{self.pk}/{str(uuid.uuid4())}.png'


def get_default_profile_image_path():
    return f'profile_images/{"default_profile_image.png"}'


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default='')
    is_delete = models.CharField(max_length=50, default='')
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_image_path)
    role = models.ForeignKey('Role', related_name='users', blank=True, null=True, on_delete=models.RESTRICT)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    #FOR ADMIN PANEL
    admin = models.BooleanField(default=False)

    def has_perm(self,perm,obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.admin
    @property 
    def is_superuser(self):
        return self.admin
    #--------------------------------------------------------
