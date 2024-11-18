from django.shortcuts import render, HttpResponse

menu = [{'title': 'О сайте', 'urlname': 'about'},
        {'title': 'Добавить статью', 'url_name': 'PostForm'},
        {'title': 'Войти', 'urlname': 'login'},
]

def home(request):
    context = {
        'menu': menu,
    }
    return render(request, 'blog/home.html', context=context)

def pageNotFound(request, exception):
    return HttpResponse('Page not found')