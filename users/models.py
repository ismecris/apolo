from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        AGENT = 'agent', 'Atendente'
        USER  = 'user',  'Usuário'

    role       = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    department = models.CharField(max_length=100, blank=True)
    avatar     = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Resolve o conflito de reverse accessor
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_agent(self):
        return self.role == self.Role.AGENT

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN