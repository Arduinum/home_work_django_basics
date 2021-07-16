from django.db import models

# тут обращение к базе данных на классах

class ProductCategory(models.Model):
    # создание колонок в таблице (делать makemigrations и migrate)
    name = models.CharField(
        verbose_name='имя',
        max_length=64, 
        unique=True
    )
    description = models.TextField(
        verbose_name='описание', 
        blank=True
    )
    # автоматом ставит дату создания
    created = models.DateTimeField(
        auto_now_add=True
    ) 
    # дата обновления записи
    updated = models.DateTimeField(
        auto_now=True
    ) 
    is_deleted = models.BooleanField(default=False)

    # не делать makemigrations и migrate (редактирование ниже)
    # переопределили метод (будет указано название категории продукта)
    def __str__(self):
        return self.name or f'Category with id - {self.pk}'
    
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, # модель для связи
        on_delete=models.CASCADE, # каскадно удаление дочерних если удалить основной
        verbose_name='категория',
    )
    # создание колонок в таблице (делать makemigrations и migrate)
    name = models.CharField(
        verbose_name='имя продукта',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='product_images',
        blank=True, # может быть пустым
        verbose_name='изображение',
    )
    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=100,
        blank=True,
    )
    description = models.TextField(
        verbose_name='описание', 
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8, # максимум колличество цифр в числе
        decimal_places=2, # колличество знаков после запятой
        default=0,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество товара на складе',
        default=0,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    ) # автоматом ставит дату создания
    updated = models.DateTimeField(
        auto_now=True,
    ) # дата обновления записи

    # не делать makemigrations и migrate (редактирование ниже)
    # переопределили метод (будет указано название категории продукта)
    def __str__(self):
        return self.name or f'Product with id - {self.pk}'
    
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'