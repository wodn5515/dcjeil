from rest_framework import serializers
from board.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()

    def get_writer(self, obj):
        return "관리자" if obj.writer.is_superuser else obj.writer

    class Meta:
        model = Comment
        fields = ("writer", "content", "date")