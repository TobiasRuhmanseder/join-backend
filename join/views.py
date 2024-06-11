from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from join.models import Board, TaskCategory
from join.models import Task
from join.serializers import BoardSerializer
from join.serializers import TaskSerializer
from join.permissions import IsBoardUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import TaskCategorySerializer, UserCreateSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

"""
    Handles user authentication and token generation.
    
    Methods:
        post: Authenticates the user and returns an authentication token.
"""
class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request}) 
        if not serializer.is_valid():
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })

"""
    Handles displaying and managing boards.
    
    Methods:
        get: Returns a list of boards associated with the authenticated user.
        
    Permissions:
        Requires the user to be authenticated and to have access to the board.
"""
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('-created_at')
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardUser]

    def get(self, request, format=None):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True, context={'request': request})
        return Response(serializer.data)
    

"""
    Handles displaying and managing tasks.
    
    Methods:
        get: Returns a list of tasks.
        
    Permissions:
        Requires the user to be authenticated.
"""
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

"""
    API View to create a new user.
    """
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


"""
    A viewset for viewing and editing user instances.
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

"""
    A view for getting the current User data.
"""
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

"""
    A viewset for viewing and editing task categories.
"""
class TaskCategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [IsAuthenticated]