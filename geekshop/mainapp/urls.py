from django.urls import path
from .views import products

app_name = 'products'  # имя для приложения

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
]
