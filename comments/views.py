from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class   = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(ticket_id=self.kwargs['ticket_id']).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ticket_id=self.kwargs['ticket_id'])