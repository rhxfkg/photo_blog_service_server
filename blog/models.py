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

    def save(self, *args, **kwargs):
        # 중복된 태그 제거
        if isinstance(self.tags, list):  # tags가 리스트인지 확인
            self.tags = list(set(self.tags))
        super().save(*args, **kwargs)  # 부모 클래스의 save 호출

    def __str__(self):
        return self.title
