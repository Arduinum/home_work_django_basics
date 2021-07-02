from django.shortcuts import render
from mainapp.models import Product 

def index(request):  # request - словарь прилетающий на сервак
    title = 'магазин'
    products = Product.objects.all()[:5]
    context = {
        'title': title,
        'products': products
    }
    # рендерим нашу html
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
