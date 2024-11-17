from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('Post', views.BlogImages)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('favorites/', views.favorite_list, name='favorite_list'),  # 즐겨찾기 목록 페이지
    path('post/<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),  # 즐겨찾기 토글 API
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 게시물 수정 경로
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('js_test/', views.js_test, name='js_test'),
    path('api_root/', include(router.urls)),
] 