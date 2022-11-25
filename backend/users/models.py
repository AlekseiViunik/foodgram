from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=50,
        unique=True,
    )
    email = models.EmailField(
        'Email',
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}, {self.email}'
