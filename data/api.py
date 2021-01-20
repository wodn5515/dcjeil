from rest_framework import viewsets, generics
from board.models import Comment
from .serializers import CommentSerializer

class CommentList(generics.ListAPIView):
    """
    댓글 DRF
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs["post"]
        return Comment.objects.filter(post=post_pk)