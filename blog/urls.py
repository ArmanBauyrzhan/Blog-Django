from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('view-post', post_list, name='view-post'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create-post/', create_post, name='create-post'),
]