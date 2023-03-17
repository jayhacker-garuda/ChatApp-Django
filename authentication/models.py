from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from core import models as core_models
# Create your models here.


class ChatUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # print('creating user')

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser has to have is_staff True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("superuser has to have is_superuser True")

        return self.create_user(email=email, password=password, **extra_fields)


class ChatUser(core_models.BaseModel,AbstractUser):
    """Chat User Model

    """
    email = models.EmailField(_("email address"), blank=False, unique=True, error_messages={
        "unique": _("A user with that email already exists."),
    },)
    objects = ChatUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.email
