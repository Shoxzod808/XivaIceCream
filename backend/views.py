from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Product, Driver, Inventory, InventoryProduct
from .models import Order, OrderProduct
from .utils import refresh_count_for_products

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods



from django.http import HttpResponseRedirect

@csrf_exempt
@require_http_methods(["POST"])
def process_products(request):
    if request.method == 'POST':
        # Получите данные из запроса
        data = json.loads(request.body)
        products = data.get('products')
        driver_id = data.get('driverId')
        status = False
        order = None
        driver = Driver.objects.get(id=driver_id)
        cash = 0
        print(data)
        for data in products:
            if 'count' in data and data['count'] != '' and int(data['count']) > 0:
                product = Product.objects.get(name=data['name'])
                if product.count < int(data['count']):
                    raise ValueError()
        for data in products:
            if 'count' in data and data['count'] != '' and int(data['count']) > 0:
                if not status:
                    order = Order.objects.create(
                    driver=driver,
                    )
                    status = True
                product = Product.objects.get(name=data['name'])
                order_product = OrderProduct.objects.create(
                    product=product,
                    count=int(data['count']),
                    order=order,
                    price=data['price'],
                )
                print(order_product.count * order_product.price * product.case, order_product.count, product.price, product.case  )
                cash += int(order_product.count) * int(order_product.price) * product.case
        order.cash = cash
        order.save()
        refresh_count_for_products()
        if not status :
            raise ValueError
        return HttpResponseRedirect(f'/document/{order.id}')  # Замените '/success/' на URL вашего редиректа
    else:
        return JsonResponse({'error': 'Invalid request method or not an AJAX request.'}, status=400)

@login_required
def document(request, id=1):
    context = dict()
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'document.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")


@csrf_exempt  # Отключаем CSRF защиту для этого запроса
@require_http_methods(["POST"])  # Разрешаем только POST запросы
def save_products(request):
    try:
        data = json.loads(request.body)  # Преобразуем JSON из тела запроса в Python словарь
        products = data.get('products')
        
        status = False
        inventory = None
        for data in products:
            if 'quantity' in data and int(data['quantity']) > 0:
                if not status:
                    inventory = Inventory.objects.create()
                    status = True
                product = Product.objects.get(name=data['name'])
                inventory_product = InventoryProduct.objects.create(
                    product=product,
                    count=int(data['quantity']),
                    inventory=inventory
                )
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
    refresh_count_for_products()
    context = dict()
    context['products'] = list(Product.objects.filter(count__gt=0))
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
    drivers = list(Driver.objects.all())

    
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
    driver = Driver.objects.get(id=id)
    context = dict()
    context['products'] = list(Product.objects.filter(count__gt=0))
    context['driver'] = driver
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'driver.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    

@login_required
def finance(request):
    orders_all = Order.objects.all()
    orders_1 = Order.objects.filter(status='Yakunlandi')
    orders_2 = Order.objects.filter(status='Jarayonda')
    context = dict()
    context['orders_all'] = orders_all
    context['orders_1'] = orders_1
    context['orders_2'] = orders_2
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def order_detail(request, id=1):
    context = dict()
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'order_detail.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
