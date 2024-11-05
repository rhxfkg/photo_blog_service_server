from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


class BlogImages(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def favorite_list(request):
    favorites = Post.objects.filter(is_favorited=True)
    return render(request, 'blog/favorite_list.html', {'favorites': favorites})

@api_view(['POST'])
def toggle_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_favorited = not post.is_favorited
    post.save()
    return Response({'is_favorited': post.is_favorited})

def post_detail(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                post.author, _ = User.objects.get_or_create(username='default_user', defaults={'password': 'temporary_password'})
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    # post 객체를 템플릿에 전달
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@require_POST  # POST 요청만 허용
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')  # 삭제 후 기본 페이지로 리디렉션

def js_test(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post_data = []

    for post in posts:
        post_data.append({
            'id': post.id,
            'title': post.title,
            'text': post.text,  # 'content' 대신 'text' 사용
            'image_url': post.image.url if post.image else None,
            'published_date': post.published_date,
            'is_favorited': post.is_favorited,  # 즐겨찾기 필드 추가
        })

    return JsonResponse(post_data, safe=False)
