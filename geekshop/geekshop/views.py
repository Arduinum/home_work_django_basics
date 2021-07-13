from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket

def index(request):  # request - словарь прилетающий на сервак
    title = 'магазин'
    products = Product.objects.all()[:5]
    
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    
    context = {
        'title': title,
        'products': products,
        'basket': basket
    }
    # рендерим нашу html
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
