from django.db import models
from django.conf import settings


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN        = 'open',        'Aberto'
        IN_PROGRESS = 'in_progress', 'Em andamento'
        WAITING     = 'waiting',     'Aguardando'
        RESOLVED    = 'resolved',    'Resolvido'
        CLOSED      = 'closed',      'Fechado'

    class Priority(models.TextChoices):
        LOW    = 'low',    'Baixa'
        MEDIUM = 'medium', 'Média'
        HIGH   = 'high',   'Alta'
        URGENT = 'urgent', 'Urgente'

    title       = models.CharField(max_length=200)
    description = models.TextField()
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    priority    = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} — {self.title}'