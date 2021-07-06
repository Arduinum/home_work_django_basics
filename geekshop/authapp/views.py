from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from authapp.forms import ShopUserLoginForm

# вход в аккаунт
def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    # если форма аккаунта валидная
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

    user =  auth.authenticate(username=username, password=password)
    # если user прошёл проверку подлинности и аккаунт активирован
    if user and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form # форма с логиным и паролем
    }
    # рендерим веб стр с логином и передаём контекст
    return render(request, 'authapp/login.html', context)

# выход из аккаунта
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index')) 
