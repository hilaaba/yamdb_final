from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_user

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user],
        verbose_name='Логин',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта',
    )
    bio = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        blank=True,
        default=USER,
        verbose_name='Роль',
    )

    class Meta(AbstractUser.Meta):
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
