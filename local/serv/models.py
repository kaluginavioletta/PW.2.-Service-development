from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    fio = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    consent = models.BooleanField(default=False)

    # для разрешения конфликтов обратного доступа к определенным полям
    # (groups и user_permissions, которые используются для управления группами
    # и разрешениями пользователей)
    groups = models.ManyToManyField(Group, related_name='serv_users')
    user_permissions = models.ManyToManyField(Permission, related_name='serv_users')

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
