"""
Сериализаторы для api.
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from ..posts.models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели Post."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post',)
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Group."""
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow."""
    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username',
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)

        # Защита от подписок-дубликатов.
        validators = [
            UniqueTogetherValidator
            (
                queryset=Follow.objects.all(),
                fields=('user', 'following',)
            )
        ]

    def validate_following(self, user_to_follow):
        """Метод валидации объекта подписки: нельзя подписаться на себя и
        на несуществующего автора."""
        if (
                user_to_follow == self.context['request'].user
                or not User.objects.filter(username=user_to_follow).exists()
        ):
            raise serializers.ValidationError('Невозможно подписаться на '
                                              'этого автора.')
        return user_to_follow
