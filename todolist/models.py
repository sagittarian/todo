from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


PRIORITIES_LIST = list(range(3))
PRIORITIES_NAMES = ('low', 'medium', 'high')
LOW, MEDIUM, HIGH = PRIORITIES_LIST
PRIORITIES = zip(PRIORITIES_LIST, PRIORITIES_NAMES)
REVERSE_PRIORITIES = dict(zip(PRIORITIES_NAMES, PRIORITIES_LIST))
PRIORITY_DICT = dict(PRIORITIES)
DEFAULT_PRIORITY = MEDIUM

LABEL_MAX_LEN = 255

class TodoItem(models.Model):
    label = models.CharField(max_length=LABEL_MAX_LEN)
    priority = models.IntegerField(choices=PRIORITIES,
                                   default=DEFAULT_PRIORITY)
    user = models.ForeignKey(User)

    def as_dict(self):
        return {
            'id': self.pk,
            'label': self.label,
            # 'priority': self.priority,
            'priority': PRIORITY_DICT[self.priority],
        }

    def __unicode__(self):
        return 'label: {}, priority: {}, user: {}'.format(self.label,
                                                          self.priority,
                                                          self.user)

    class Meta:
        verbose_name = 'Todo Item'
        verbose_name_plural = 'Todo Items'


admin.site.register(TodoItem)
