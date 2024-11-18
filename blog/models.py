from django.db import models
from django.contrib.auth.models import User

# Модель Post
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)  # Публичный или скрытый пост
    is_visible_on_request = models.BooleanField(default=False)  # Скрытый пост (по запросу)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)  # Теги для постов

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.all()

# Модель Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий к посту {self.post.title} от {self.user.username}"

# Модель Tag
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

# Модель Subscription
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber.username} подписан на {self.subscribed_to.username}"
