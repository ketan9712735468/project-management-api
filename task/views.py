from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from task.models import Task
from task.serializers import TaskSerializer
from django.http import Http404
from comment.models import Comment
from comment.serializers import CommentSerializer

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        """Retrieve a specific task."""
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update task details."""
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")

        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Delete a task."""
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Custom action for listing and creating comment for a specific task
    @action(detail=True, methods=['get', 'post'], url_path='comments', permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        try:
            task = Task.objects.get(id=pk)
        except:
            return Response({"message":"Task not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle GET (List comments for this task)
        if request.method == 'GET':
            tasks = Comment.objects.filter(task=task)
            serializer = CommentSerializer(tasks, many=True)
            return Response(serializer.data)

        # Handle POST (Create a new comment for this task)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
