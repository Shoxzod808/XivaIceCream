from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Product, Driver

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt  # Отключаем CSRF защиту для этого запроса
@require_http_methods(["POST"])  # Разрешаем только POST запросы
def save_products(request):
    try:
        data = json.loads(request.body)  # Преобразуем JSON из тела запроса в Python словарь
        products = data.get('products')
        # Обработка данных
        return JsonResponse({'status': 'success', 'message': 'Malumotlar saqlandi'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})


def logout_view(request):
    logout(request)
    return redirect('login') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неправильный логин или пароль'})
    else:
        return render(request, 'login.html')

@login_required
def index(request):
    context = dict()
    context['products'] = list(Product.objects.filter(count__gt=0))*25
    context['summa'] = 0
    for i in Product.objects.all():
        context['summa'] += i.total_price()
    context['count'] = 0
    for i in Product.objects.all():
        context['count'] += i.count
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'index-1.html', context)
    # Проверяем, принадлежит ли пользователь к группе "Менеджер"
    elif request.user.groups.filter(name='Менеджер').exists():
        return render(request, 'index-2.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def kirim(request):
    context = dict()
    context['products'] = list(Product.objects.all())
    context['summa'] = 0
    for i in Product.objects.all():
        context['summa'] += i.total_price()
    context['count'] = 0
    for i in Product.objects.all():
        context['count'] += i.count
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'kirim.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def chiqim(request):
    drivers = list(Driver.objects.all())*15
    context = {
        'id': 1,
        'drivers': drivers,
    }
    print(drivers)
    
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'chiqim.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    
@login_required
def driver(request, id=1):
    drivers = Driver.objects.all()
    context = {
        'id': 1,
        'drivers': drivers,
    }
    print(drivers)
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'driver.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")