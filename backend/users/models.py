from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import TokenProxy, Token
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Уникальное имя пользователя',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    is_staff = models.BooleanField(
        verbose_name='Администратор',
        default=False
    )
    is_blocked = models.BooleanField(
        verbose_name='Заблокирован',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class MyToken(Token):
    
    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'


class MyTokenProxy(TokenProxy):

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'