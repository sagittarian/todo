from django.db import models
from django.contrib.auth.models import User

PRIORITIES = (
    (0, 'low'),
    (1, 'medium'),
    (2, 'high')
)

class TodoItem(models.Model):
    label = models.CharField(max_length=255)
    priority = models.IntegerField(choices=PRIORITIES)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return 'label: {}, priority: {}, user: {}'.format(self.label,
                                                          self.priority,
                                                          self.user)

    class Meta:
        verbose_name = 'Todo Item'
        verbose_name_plural = 'Todo Items'
