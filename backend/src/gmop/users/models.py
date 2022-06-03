from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

import gmop.core.messages as messages


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name=None,
        last_name=None,
        email=None,
        company=None,
        access_group=None,
        is_active=None,
        password=None,
    ):
        if email is None:
            raise TypeError(messages.EMAIL_ADDRESS_NOT_PROVIDED_ERR_MSG)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            company=company,
            access_group=access_group,
            is_active=is_active if is_active else False,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError(messages.PASSWORD_NOT_PROVIDED_ERR_MSG)

        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True)
    company = models.CharField(max_length=255, null=True)

    access_group = models.CharField(max_length=255, null=True)

    username = None
    date_joined = None
    last_login = None

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
