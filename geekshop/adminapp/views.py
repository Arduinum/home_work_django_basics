from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


# реализация на Function Based Views
# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'

#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

#     context = {
#         'title': title,
#         'objects': users_list
#     }

#     return render(request, 'adminapp/users.html', context)

# ListView - для вывода списка объектов
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects' # если не задать будет object_list
    paginate_by = 3 # сколько записей выводить на 1й стр

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'

        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

# def user_create(request):
#     title = 'пользователи/создать'

#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)

#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()

#     context = {
#         'title': title,
#         'user_form': user_form
#     }

#     return render(request, 'adminapp/user_create.html', context)


# CreateView - для создания объектов
class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "adminapp/user_create.html"
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'

        return context


def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'title': title,
        'user_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', context)


# моя попытка пока не доделана закоментировал
# class UserUpdateView(UpdateView):
#     model =
#     form_class = 
#     template_name = 'adminapp/user_update.html'
#     success_url = '/'

#     def get_object(self, queryset=None):
   
#         if queryset is None:
#             queryset = self.get_queryset()
    
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         slug = self.kwargs.get(self.slug_url_kwarg)
#         if pk is not None:
#             queryset = queryset.filter(pk=pk)
    
#         if slug is not None and (pk is None or self.query_pk_and_slug):
#             slug_field = self.get_slug_field()
#             queryset = queryset.filter(**{slug_field: slug})
    
#         if pk is None and slug is None:
#             raise AttributeError(
#                 "Generic detail view %s must be called with either an object "
#                 "pk or a slug in the URLconf." % self.__class__.__name__
#             )
#         try:
#             obj = queryset.get()
#         except queryset.model.DoesNotExist:
#             raise Http404(("No %(verbose_name)s found matching the query") % 
#                             {'verbose_name': queryset.model._meta.verbose_name})
#         return obj

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().post(request, *args, **kwargs)

    # if post():
    #     pass

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(UserUpdateView, self).get_context_data()
    #     context['title'] = 'пользователи/редактирование'

    #     return context


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_deleted = True
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'

#     categories_list = ProductCategory.objects.all()

#     context = {
#         'title': title,
#         'objects': categories_list
#     }

#     return render(request, 'adminapp/categories.html', context)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    # paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data()
        context['title'] = 'админка/категории'

        return context

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('name')


# def category_create(request):
#     title = 'категории/создать'

#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)

#         if category_form.is_valid():
#             category_form.save()
        
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
        
#     context = {
#         'title': title,
#         'category_form': category_form
#     }

#     return render(request, 'adminapp/category_create.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = "adminapp/category_create.html"
    context_object_name = 'objects'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data()
        context['title'] = 'категории/создать'

        return context


# def category_update(request, pk):
#     title = 'категории/редактирование'
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'category_form': edit_form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


def category_delete(request, pk):
    title = 'категории/удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_deleted = True
        category.delete()
        category.save()
        
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_delete': category
    }

    return render(request, 'adminapp/category_delete.html', context)


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'продукты/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': category,
    }

    return render(request, 'adminapp/product_create.html', context)


def product_read(request, pk):
    title = 'продукты/подробнее'
    product = get_object_or_404(Product, pk=pk)
    context = {'title': title, 'product': product}

    return render(request, 'adminapp/product_read.html', context)


def product_update(request, pk):
    title = 'продукты/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category,
        'product': edit_product,
    }

    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_deleted = True
        product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product
    }

    return render(request, 'adminapp/product_delete.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product_set.update(is_deleted=True)
    else:
        instance.product_set.update(is_deleted=False)

    db_profile_by_type(sender, 'UPDATE', connection.queries)
