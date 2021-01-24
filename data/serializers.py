from rest_framework import serializers
from board.models import Comment, Post

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()

    def get_writer(self, obj):
        return "관리자" if obj.writer.is_superuser else obj.writer.name
        
    class Meta:
        model = Comment
        read_only_fields = ("id", "writer", "date")
        fields = ("id", "content", "writer", "date")

    