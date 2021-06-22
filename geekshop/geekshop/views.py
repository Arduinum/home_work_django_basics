from django.shortcuts import render


def index(request):  # request - словарь прилетающий на сервак
    return render(request, 'index.html')  # рендерим нашу html


def contacts(request):
    return render(request, 'contact.html')
