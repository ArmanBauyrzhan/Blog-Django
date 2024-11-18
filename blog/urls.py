from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('view-post', post_list, name='view-post'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-post/', create_post, name='create-post'),
    path('profile/<str:username>/', profile, name='profile'),
    path('post/<slug:slug>/', post_detail, name='post-detail'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
    path('post/edit/<slug:slug>/', edit_post, name='edit-post'),
    path('post/delete/<slug:slug>/', delete_post, name='delete-post'),
    path('posts/', posts_by_tag, name='all-posts'),
    path('posts/tag/<slug:tag_slug>/', posts_by_tag, name='posts-by-tag'),
]