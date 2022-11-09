"""
Вьюсеты api.
"""
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Follow, User
from api.serializers import (PostSerializer, GroupSerializer,
                             CommentSerializer, FollowSerializer)
from api.permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохранение юзера в качестве автора создаваемого поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AuthorOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Создает queryset комментариев поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        comments = post.comments.all()
        return comments

    def perform_create(self, serializer):
        """
        Сохранение юзера в качестве автора добавляемого комментария к
        соответстующему посту.
        ."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Follow."""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Создает queryset подписок."""
        follows = Follow.objects.filter(user=self.request.user)
        return follows

    def perform_create(self, serializer):
        """Сохранение подписки на автора юзером."""
        username_to_follow = serializer.initial_data.get('following')
        user_to_follow = get_object_or_404(User, username=username_to_follow)
        serializer.save(user=self.request.user, following=user_to_follow)
