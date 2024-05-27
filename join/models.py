import datetime
from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    created_at = models.DateField(("Date"), default=datetime.date.today)
    users = models.ManyToManyField(User, related_name="boards")

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    created_at = models.DateField(("Date"), default=datetime.date.today)
    priority = models.CharField(max_length=20, default='todo')
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='tasks') 
    subtasks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title