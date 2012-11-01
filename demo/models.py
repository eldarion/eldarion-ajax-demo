from django.db import models

from django.contrib.sessions.models import Session


class Task(models.Model):
    
    session = models.ForeignKey(Session)
    label = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
