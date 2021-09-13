from rest_framework.serializers import ModelSerializer

from tasks.models import Task


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'delivery_date')

    def create(self, validated_data):
        task = Task.objects.create(
            **validated_data,
            user=self.context['request'].user
        )
        return task
