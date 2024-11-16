from blog.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image', 'published_date', 'is_favorited', 'author']
