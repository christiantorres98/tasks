from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class Status(models.TextChoices):
        complete = 'completa', _('complete')
        incomplete = 'incompleta', _('incompleted')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    status = models.CharField(max_length=15, verbose_name=_('status'), choices=Status.choices,
                              default=Status.incomplete)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    delivery_date = models.DateTimeField(_('delivery date'))

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.name
