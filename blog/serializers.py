from blog.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)  # tags 필드 추가


    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'published_date', 'is_favorited', 'author', 'tags']
