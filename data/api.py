from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import HttpResponse
from board.models import Comment, Post
from .serializers import CommentSerializer
from .permissions import CommentPermission


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 DRF
    """
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)

    def get_queryset(self):
        post_pk = self.kwargs["post"]
        return Comment.objects.filter(post=post_pk)

    def create(self, request, *args, **kwargs):
        post_pk = self.kwargs["post"]
        post = Post.objects.get(pk=post_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, writer=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
