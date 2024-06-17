
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
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action


class LoginView(ObtainAuthToken):
    """
    Handles user authentication and token generation.
    
    Methods:
        post: Authenticates the user and returns an authentication token.
    """
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

class BoardViewSet(viewsets.ModelViewSet):
    """
    Handles displaying and managing boards.
    
    Methods:
        get: Returns a list of boards associated with the authenticated user.
        
    Permissions:
        Requires the user to be authenticated and to have access to the board.
    """
    queryset = Board.objects.all().order_by('-created_at')
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated,] #Use "isboardUser" permission when expanding to multiple boards

    @action(detail=False, methods=['post'], url_path='check_board_default', permission_classes=[AllowAny], authentication_classes = [])
    def check_and_create_board(self, request):
        """
        check if a Baord with a specific ID exists, and create it if it doesn't.
        """
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error': 'Board ID ist required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            board = Board.objects.get(id=board_id)
            return Response({'message': f'Board with id {board_id} already exists', 'board': board.id, 'title': board.title})
        except Board.DoesNotExist:
            title = request.data.get('title', 'Default Board')
            description = request.data.get('description', f'This is the default Board with the ID')
            board = Board(id=board_id, title=title, description=description)
            board.save(force_insert=True)
            serializer = BoardSerializer(board)
            return Response({'message': f'Board with id {board_id} created', 'board': serializer.data}, status=status.HTTP_201_CREATED)

class TaskViewSet(viewsets.ModelViewSet):
    """
    Handles displaying and managing tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    """
    API View to create a new user.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CurrentUserView(APIView):
    """
    A view for getting the current User data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class GuestUserExistsView(APIView):
    """
    A view for checking the exists from a guest user
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def get(self, request):
        exists = User.objects.filter(username='guest').exists()
        return Response({'exists': exists}, status=status.HTTP_200_OK)

class TaskCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task categories.
    """
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [IsAuthenticated]