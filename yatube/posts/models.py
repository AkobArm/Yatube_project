from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст Поста',
        help_text='Текст нового поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        help_text='Группа, к которой будет относиться пост',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа'
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        default_related_name = "posts"
