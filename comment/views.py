from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from comment.models import Comment
from comment.serializers import CommentSerializer

class CommentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        """Retrieve details of a specific comment."""
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404("Comment not found")
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update comment details."""
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            raise Http404("Comment not found")

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Delete a comment."""
        try:
            comment = Comment.objects.get(pk=pk, user=request.user)
        except Comment.DoesNotExist:
            raise Http404("Comment not found")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
