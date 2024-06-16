from django.contrib.auth.models import User
from rest_framework import serializers
from join.models import Board, TaskCategory
from join.models import Task

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Board model.  
    """
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    
    class Meta:
        model = Board
        fields = ['id','title','description','created_at','users']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Task model. 
    """
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=TaskCategory.objects.all())
    class Meta:
        model = Task
        fields = ['id','title','description','users','due_date','priority','category','board','subtasks', 'status']
                    #Wenn ich __all__ verwende, dann gibt er mir anstatt der id den URL Pfad ../tasks/id zurück, so bekomme ich die id einzeln
class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """ 
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class TaskCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Categories from the tasks.
    """   
    class Meta:
        model = TaskCategory
        fields = ['id', 'category', 'color']