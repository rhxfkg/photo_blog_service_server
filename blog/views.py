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
from django.db.models import Q  # Q 객체는 OR 조건을 지원합니다.
from django.views.decorators.csrf import csrf_exempt
from .models import Post  # 모델 임포트 추가
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

class BlogImages(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else User.objects.get_or_create(username='default_user')[0]
        serializer.save(author=user)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # 로그인 성공 시 post_list 페이지로 이동
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
def get_image_list(request):
    """
    이미지 목록을 반환하는 API
    """
    posts = Post.objects.filter(published_date__lte=timezone.now())
    image_list = [
        {
            "id": post.id,
            "file": post.image.url if post.image else None,
        }
        for post in posts
    ]
    return JsonResponse(image_list, safe=False)


@api_view(['POST'])
@csrf_exempt
def add_tags_to_image(request, pk):
    """
    태그 추가 API: 검출된 객체를 받아 해당 이미지의 태그를 업데이트
    """
    post = get_object_or_404(Post, pk=pk)
    tags = request.data.get("tags", [])
    if tags:
        if not post.tags:
            post.tags = []
        post.tags += tags  # 태그 추가
        post.save()
        return Response({"status": "success", "tags": post.tags})
    return Response({"status": "failed", "message": "No tags provided."}, status=400)

# 80개 카테고리 리스트 정의
CATEGORIES = sorted([
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", 
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", 
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", 
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", 
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", 
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", 
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", 
    "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", 
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", 
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush", "no tag"
])

def category_list(request):
    return render(request, 'blog/category_list.html', {'categories': CATEGORIES})

def filtered_images(request):
    category = request.GET.get('category')  # URL의 GET 파라미터에서 'category' 값을 가져옵니다.
    if category:  # 카테고리 값이 존재할 때만 필터링
        images = Post.objects.filter(tags__icontains=category)
    else:  # 카테고리 값이 없으면 전체 이미지 반환
        images = Post.objects.all()
    return render(request, 'blog/filtered_images.html', {'category': category, 'images': images})

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
            post.author = request.user if request.user.is_authenticated else User.objects.get_or_create(username='default_user')[0]
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
            post.author = request.user if request.user.is_authenticated else User.objects.get_or_create(username='default_user')[0]
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

def post_search(request):
    query = request.GET.get('q', '')  # 'q'는 검색창에 입력된 검색어를 받습니다.
    if query:
        posts = Post.objects.filter(Q(title__icontains=query), published_date__lte=timezone.now()).order_by('published_date')
    else:
        posts = Post.objects.none()  # 검색어가 없으면 빈 결과 반환
    return render(request, 'blog/post_search.html', {'posts': posts, 'query': query})

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
