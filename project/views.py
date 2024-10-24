from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project.serializers import ProjectSerializer
from task.models import Task
from task.serializers import TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the owner to the current authenticated user
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Return only the projects owned by the authenticated user
        user = self.request.user
        return Project.objects.filter(owner=user)

    # Custom action for listing and creating tasks for a specific project
    @action(detail=True, methods=['get', 'post'], url_path='tasks', permission_classes=[permissions.IsAuthenticated])
    def tasks(self, request, pk=None):
        project = self.get_object()

        # Handle GET (List tasks for this project)
        if request.method == 'GET':
            tasks = Task.objects.filter(project=project)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        # Handle POST (Create a new task for this project)
        elif request.method == 'POST':
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
