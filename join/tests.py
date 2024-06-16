# tests.py
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Task, Board, TaskCategory
from django.contrib.auth.models import User
import datetime

class TaskAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = TaskCategory.objects.create(category='Work', color='blue')
        self.board = Board.objects.create(title='Board 1', description='Test Board')
        self.board.users.add(self.user)
        self.task_data = {
            "title": "Test Task",
            "description": "",
            "priority": "medium",
            "category": self.category.id,
            "board": self.board.id,
            "status": "todo",
            "users": [self.user.id],
            "due_date": datetime.date.today().isoformat()
        }

    def test_create_task(self):
        response = self.client.post(reverse('task-list'), self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')

    def test_list_tasks(self):
        Task.objects.create(title='Task 1', description='First task', category=self.category, board=self.board, status='todo')
        Task.objects.create(title='Task 2', description='Second task', category=self.category, board=self.board, status='todo')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_task(self):
        task = Task.objects.create(title='Task 1', description='First task', category=self.category, board=self.board, status='todo')
        response = self.client.get(reverse('task-detail', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_update_task(self):
        task = Task.objects.create(title='Task 1', description='First task', category=self.category, board=self.board, status='todo')
        update_data = {
            "title": "Updated Task",
            "description": "Updated task description",
            "priority": "medium",  
            "category": self.category.id,
            "board": self.board.id,
            "status": "todo",
            "users": [self.user.id],
            "due_date": datetime.date.today().isoformat(),
            "subtasks": []  
        }
        response = self.client.put(reverse('task-detail', args=[task.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(title='Task 1', description='First task', category=self.category, board=self.board, status='todo')
        response = self.client.delete(reverse('task-detail', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

class BoardAPITests(APITestCase):
    def test_check_and_create_board(self):
        url = '/api/boards/check_board_default/'
        response = self.client.post(url, {"id": 1, "title": "Default Board", "description": "Board description"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Board.objects.get().title, 'Default Board')