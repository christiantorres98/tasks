from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task
from tasks.serializers import TaskModelSerializer


class TaskTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user(
            username='test_1',
            email='test_1@test.com',
            password='test123**.'
        )
        self.user_2 = User.objects.create_user(
            username='test_2',
            email='test_2@test.com',
            password='test123**.'
        )
        self.task1 = G(Task, user=self.user_1)
        self.task2 = G(Task, user=self.user_2)
        self.task3 = G(Task, user=self.user_1, name='task 3',
                       description='description of task 3')

    def test_list_own_tasks_not_authenticated(self):
        url = reverse('tasks:task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_own_tasks(self):
        url = reverse('tasks:task-list')
        self.client.force_authenticate(self.user_1)
        response = self.client.get(url)
        tasks = self.user_1.task_set.all()
        serializer = TaskModelSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), tasks.count())
        self.assertEqual(response.data['results'], serializer.data)

    def test_list_tasks_with_search(self):
        url = reverse('tasks:task-list') + '?search=task 3'
        self.client.force_authenticate(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_task_creation_not_authenticated(self):
        url = reverse('tasks:task-list')
        payload = {
            'name': 'test task',
            'description': 'test task description',
            'delivery_date': "12/09/2021 13:56:24"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_failed_task_creation_by_missing_data(self):
        url = reverse('tasks:task-list')
        self.client.force_authenticate(self.user_1)
        payload = {
            'name': 'test task',
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_task_creation(self):
        url = reverse('tasks:task-list')
        self.client.force_authenticate(self.user_1)
        payload = {
            'name': 'test task',
            'description': 'test task description',
            'delivery_date': "12/09/2021 13:56:24"
        }
        response = self.client.post(url, payload)
        task = Task.objects.get(id=response.data['id'])
        serializer_data = TaskModelSerializer(task).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in payload.keys():
            self.assertEqual(payload[key], serializer_data[key])

    def test_task_deletion_not_authenticated(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_deletion_without_permission(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_task_deletion(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_update_not_authenticated(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_update_without_permission(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_2)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_update(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_1)
        payload = {
            'name': 'updated task',
            'description': 'updated task description',
            'delivery_date': '12/09/2021 13:56:2',
            'status': 'completa'
        }
        response = self.client.put(url, payload)
        self.task1.refresh_from_db()
        serializer = TaskModelSerializer(self.task1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_task_partial_update_not_authenticated(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_partial_update_without_permission(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_2)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_partial_update(self):
        url = reverse('tasks:task-detail', args=[self.task1.pk])
        self.client.force_authenticate(self.user_1)
        payload = {'status': 'completa'}
        response = self.client.patch(url, payload)
        self.task1.refresh_from_db()
        serializer = TaskModelSerializer(self.task1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
