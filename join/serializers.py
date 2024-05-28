from django.contrib.auth.models import User
from rest_framework import serializers

from join.models import Board
from join.models import Task


"""
    Serializer for the Board model.
    
    Attributes:
        id (int): The ID of the board.
        title (str): The title of the board.
        description (str): The description of the board.
        created_at (date): The creation date of the board.
        users (list): The users associated with the board.
"""
class BoardSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    
    class Meta:
        model = Board
        fields = ['id','title','description','created_at','users']


"""
    Serializer for the Task model.
    
    Attributes:
        id (int): The ID of the task.
        title (str): The title of the task.
        description (str): The description of the task.
        created_at (date): The creation date of the task.
        priority (str): The priority level of the task.
        board (int): The ID of the board associated with the task.
        users (list): The users associated with the task.
        subtasks (str): The subtasks within the task.
    """
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = Task
        fields = ['id','title','description','created_at','priority','board','users','subtasks']

