"""
Сериализаторы для api.
"""
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Post, Comment, Group, Follow


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
    class Meta:
        model = Follow
        fields = ('user', 'following',)
        read_only_fields = ('user',)
