from django.shortcuts import render


def index(request):  # request - словарь прилетающий на сервак
    title = 'магазин'
    context = {
        'title': title
    }
    # рендерим нашу html
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
