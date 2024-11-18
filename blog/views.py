from msilib.schema import CustomAction

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserCreationForm, PostForm

menu = [{'title': 'Главная', 'url_name': 'home'},
        {'title': 'Все посты', 'url_name': 'view-post'},
        {'title': 'Создать пост', 'url_name': 'create-post'},
]

def home(request):
    context = {
        'menu': menu,
    }
    return render(request, 'blog/home.html', context=context)

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

def pageNotFound(request, exception):
    return HttpResponse('Page not found')