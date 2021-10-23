from django.contrib.auth import get_user_model
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        read_only_fields = ('id',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        read_only=False, slug_field='username', queryset=User.objects.all()
    )
    user = serializers.ReadOnlyField(source='user.username')

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!!')
        if Follow.objects.filter(user=self.context['request'].user,
                                 following=data['following']).exists():
            raise serializers.ValidationError(
                'Подписка уже существует!!')
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
