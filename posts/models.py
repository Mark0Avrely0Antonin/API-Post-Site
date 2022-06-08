from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length = 100, verbose_name = 'Имя')
    url = models.URLField(verbose_name = 'Ссылка')
    poster = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Постер')
    created = models.DateTimeField(auto_now_add = True, verbose_name = "Дата поста")

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Голосователь')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = 'Пост голосователя')

    class Meta:
        verbose_name = 'Голосователь'
        verbose_name_plural = 'Голосователи'

    def __str__(self):
        return f'{self.voter} - {self.post}'