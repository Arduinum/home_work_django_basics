import os
import json

# from django.contrib.auth.models import User # модель чтоб создать user
from django.core.management.base import BaseCommand # класс который создаёт механику команд


from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


JSON_PATH = 'mainapp/jsons' # путь до json

# функция для чтения json
def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='UTF-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete() # почистили нашу модель
        for category in categories:
            new_category = ProductCategory(**category) # ** - распаковка
            new_category.save() # сораняем изменения в таблице
        
        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_category = Product(**product)
            new_category.save()
        
        # создаём пользователя
        super_user = ShopUser.objects.create_superuser('admin', 'admin@geekshop.local', '123', age='30')
        