from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from join.models import Board, Task
from rest_framework.authtoken.models import Token

class AuthTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login(self):
        response = self.client.post(reverse('api_token_auth'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class BoardViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.board = Board.objects.create(
            title='Test Board',
            description='A test board',
        )
        self.board.users.add(self.user)

    def test_get_boards(self):
        response = self.client.get(reverse('board_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Board')

class TaskViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.board = Board.objects.create(
            title='Test Board',
            description='A test board',
        )
        self.board.users.add(self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='A test task',
            priority='High',
            board=self.board,
        )
        self.task.users.add(self.user)

    def test_get_tasks(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')
