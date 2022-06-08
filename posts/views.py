from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response

from posts.serializers import PostSerializer, VoteSerializer
from posts.models import Post, Vote
from posts.permissions import PermissionPost


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    model = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    model = Post
    serializer_class = PostSerializer
    permission_classes = (PermissionPost, )


class VoteCreate(generics.CreateAPIView, generics.RetrieveAPIView, DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])

        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Ты уже проголосовал за этот пост :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Ты никогда не голосовал за этот пост....глупый')
