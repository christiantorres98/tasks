from django.urls import path, include
from rest_framework.routers import SimpleRouter

from tasks.viewsets import TaskModelViewSet

router = SimpleRouter()
router.register('tasks', TaskModelViewSet)

app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls))
]
