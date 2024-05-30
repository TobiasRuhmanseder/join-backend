from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from join.models import Board
from join.models import Task
from join.serializers import BoardSerializer
from join.serializers import TaskSerializer
from join.permissions import IsBoardUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

"""
    Handles user authentication and token generation.
    
    Methods:
        post: Authenticates the user and returns an authentication token.
"""
class LoginView(ObtainAuthToken):
    # serializer_class = [AuthTokenSerializer] ## man könnte zusätzlich noch einen Serializer für eine bessere Validierung verwenden

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=status.HTTP_401_UNAUTHORIZED)
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
class BoardView(APIView):
    # queryset = Board.objects.all().order_by('-created_at')
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
class TaskView(APIView):
    # queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)