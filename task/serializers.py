from rest_framework import serializers
from task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'assigned_to', 'created_at', 'due_date']
        read_only_fields = ['created_at']
