import datetime
from django.db import models
from django.contrib.auth.models import User

"""
    Represents a board which contains tasks.
    
    Attributes:
        title (str): A short title for the board.
        description (str): A detailed description of the board.
        created_at (date): The date when the board was created.
        users (ManyToManyField): A list of users associated with the board.
    """
class Board(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    created_at = models.DateField(("Date"), default=datetime.date.today)
    users = models.ManyToManyField(User, related_name="boards")

    def __str__(self):
        return self.title
    
"""
    Represents a task within a board.
    
    Attributes:
        title (str): A short title for the task.
        description (str): A detailed description of the task.
        created_at (date): The date when the task was created.
        priority (str): The priority level of the task.
        board (ForeignKey): The board to which the task belongs.
        users (ManyToManyField): A list of users associated with the task.
        subtasks (str): A list of subtasks within the task.
    """
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