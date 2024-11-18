from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import *

def home(request):
    if request.user.is_authenticated:
        # Получаем авторов, на которых подписан текущий пользователь
        subscriptions = Subscription.objects.filter(subscriber=request.user).values_list('subscribed_to', flat=True)
        # Фильтруем посты
        posts = Post.objects.filter(is_public=True) | Post.objects.filter(author__in=subscriptions).order_by('-created_at')
    else:
        # Для неавторизованных пользователей только публичные посты
        posts = Post.objects.filter(is_public=True).order_by('-created_at')

    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def post_list(request):
    return HttpResponse('Все посты')

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() # сохранение поста
            form.save_m2m() # сохранение связей с тегами
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)

    # Проверяем, подписан ли текущий пользователь на этого пользователя
    is_subscribed = Subscription.objects.filter(subscriber=request.user,
                                                subscribed_to=user).exists() if request.user.is_authenticated else False

    return render(request, 'blog/profile.html', {
        'user': user,
        'posts': posts,
        'is_subscribed': is_subscribed,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    if post.is_visible_on_request and not request.user.is_authenticated:
        messages.warning(request, 'Этот пост доступен только зарегистрированным пользователям.')
        return redirect('login')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'commnets': comments,
        'comment_form': comment_form,
    })


def subscribe(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    subscribed_user = get_object_or_404(User, id=user_id)

    if request.user == subscribed_user:
        messages.error(request, "Нельзя подписываться на самого себя!")
        return redirect('profile', username=subscribed_user.username)

    if Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_user).exists():
        messages.error(request, f"Вы уже подписаны на {subscribed_user.username}.")
    else:
        Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_user)
        messages.success(request, f"Вы подписались на {subscribed_user.username}.")

    return redirect('profile', username=subscribed_user.username)


def unsubscribe(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    subscribed_user = get_object_or_404(User, id=user_id)

    if request.user == subscribed_user:
        messages.error(request, "Нельзя отписываться от самого себя!")
        return redirect('profile', username=subscribed_user.username)

    subscription = Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_user).first()

    if subscription:
        subscription.delete()
        messages.success(request, f"Вы отписались от {subscribed_user.username}.")
    else:
        messages.error(request, f"Вы не были подписаны на {subscribed_user.username}.")

    return redirect('profile', username=subscribed_user.username)

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Получаем пост по его slug
    if request.user != post.author:  # Проверяем, что пост принадлежит текущему пользователю
        messages.error(request, "Вы не можете редактировать этот пост.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # Привязываем форму к существующему посту
        if form.is_valid():
            form.save()
            messages.success(request, "Пост успешно отредактирован.")
            return redirect('post-detail', slug=post.slug)  # Перенаправляем на страницу поста
    else:
        form = PostForm(instance=post)  # Если GET-запрос, просто показываем форму с данными поста

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Получаем пост по его slug
    if request.user != post.author:  # Проверяем, что пост принадлежит текущему пользователю
        messages.error(request, "Вы не можете удалить этот пост.")
        return redirect('home')  # Перенаправляем, если пользователь не автор поста

    post.delete()  # Удаляем пост
    messages.success(request, "Пост успешно удален.")
    return redirect('home')  # Перенаправляем на главную страницу

def pageNotFound(request, exception):
    return render(request, 'blog/page_not_found.html', {'exception': exception})