from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.permissions import IsOwner
from tasks.serializers import TaskModelSerializer


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_date", "delivery_date"]
    filter_fields = {
        "user__id": ["exact"],
        "user__username": ["exact", "icontains"],
        "status": ["exact", "icontains"],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permissions.append(IsOwner)
        return [p() for p in permissions]
