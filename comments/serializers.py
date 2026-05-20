from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_role     = serializers.CharField(source='author.role', read_only=True)

    class Meta:
        model  = Comment
        fields = ('id', 'ticket', 'author', 'author_username', 'author_role', 'content', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')