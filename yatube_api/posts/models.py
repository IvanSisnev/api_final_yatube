"""
Модели проекта.
"""
from django.contrib.auth import get_user_model
from django.db import models

# todo readme

User = get_user_model()


class Post(models.Model):
    """ Класс модели Post: посты."""
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True)

    def __str__(self):
        return self.text


class Group(models.Model):
    """ Класс модели Group: сообщества."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ Класс модели Comment: комментарии к постам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Follow(models.Model):
    """ Класс модели Follow: подписки на авторов."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
