from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_image/%Y/%m/%d/', default='blog_image/default_error.png')
    is_favorited = models.BooleanField(default=False)  # 즐겨찾기 필드 추가
    tags = models.JSONField(blank=True, default=list)  # JSONField로 태그 저장


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
