from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет автора поста(авториз.пользователь)"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """запрещает редактировать не автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        return super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """запрещает удалять не автору"""
        if serializer.author != self.request.user:
            raise PermissionDenied("Удаление контента запрещено!")
        return super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """возвращает запрос, отфильтрованный по id поста,
           к которому написаны комментарии"""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        """Сохраняет автора коммента(авториз.пользователь)"""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """запрещает редактировать не автору"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        return super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """запрещает удалять не автору"""
        if serializer.author != self.request.user:
            raise PermissionDenied("Удаление контента запрещено!")
        return super(CommentViewSet, self).perform_destroy(serializer)


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateRetrieveViewSet):

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        """возвращает запрос, отфильтрованный по юзерам,
           которые подписаны на авториз.пользователя"""
        user = get_object_or_404(User, username=self.request.user)
        return user.follower

    def perform_create(self, serializer):
        """Сохраняет подписчика(авториз.пользователь)"""
        serializer.save(user=self.request.user)
