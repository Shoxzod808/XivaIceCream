from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Product, Driver, Inventory, InventoryProduct
from .models import Order, OrderProduct, Payment, Refund, RefundProduct
from .utils import refresh_count_for_products

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .utils import calculate_driver_cash, calculate_eski_carz, calculate_payed

from django.http import HttpResponseRedirect

@csrf_exempt  # Отключаем CSRF защиту для этого запроса
@require_http_methods(["POST"])  # Разрешаем только POST запросы
def save_table_data(request):
    try:
        data = json.loads(request.body)  # Преобразуем JSON из тела запроса в Python словарь
        products = data.get('products')
        status = False
        refund = None
        for data in products:
            order = Order.objects.get(id=int(data.get('order_id')))
            if 'quantity' in data and int(data['quantity']) > 0:
                if not status:
                    refund = Refund.objects.create(order=order)
                    status = True
                product = Product.objects.get(name=data['name'])
                refund_product = RefundProduct.objects.create(
                    product=product,
                    price=data['price'],
                    count=int(data['quantity']),
                    refund=refund
                )
                
        
        # Обработка данных
        return JsonResponse({'status': 'success', 'message': 'Malumotlar saqlandi'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        payment_amount = request.POST.get('paymentAmount')
        comment_amount = request.POST.get('commentAmount')
        driver_id = request.POST.get('driverId')
        if int(payment_amount) <= 0:
            raise ValueError()
        driver = Driver.objects.get(id=driver_id)
        payment = Payment.objects.create(
            driver=driver,
            cash = int(payment_amount),
            comment = comment_amount
            )
        if payment_amount and driver_id:
            # Здесь вы можете обработать оплату и выполнить любую другую логику
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid data in POST request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


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
        for data in products:
            if 'count' in data and data['count'] != '' and int(data['count']) > 0:
                product = Product.objects.get(name=data['name'])
                if product.count < int(data['count']) or int(data['count']) < 0 or int(data['price']) < 0:
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
    if id == 1:
        order = list(Order.objects.all())[-1]
    else:
        order = Order.objects.get(id=id)
    driver = order.driver
    order_products = OrderProduct.objects.filter(order=order)
    total_sum = 0
    products = []
    for order_product in order_products:
        products.append(
            {
                'id': order_product.id,
                'product': order_product.product,
                'price': order_product.price,
                'count': order_product.count,
                'order': order_product.order,
                'cash': order_product.product.case * order_product.count * order_product.price,
            }
        )
        total_sum += order_product.product.case * order_product.count * order_product.price
    eski = calculate_eski_carz(order)
    payed = calculate_payed(order)
    context['payed'] = payed
    context['eski'] = eski
    context['products'] = products
    context['driver'] = driver
    context['total_sum'] = total_sum
    context['order'] = order
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'document.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def inventory(request, id=1):
    context = dict()
    inventory = Inventory.objects.get(id=id)
    products = InventoryProduct.objects.filter(inventory=inventory)
    total_count = 0
    for product in products:
        total_count += product.count
    context['products'] = products
    context['inventory'] = inventory
    context['total_count'] = total_count
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'inventory.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def documents(request):
    context = dict()
    orders = Order.objects.all().order_by('-created_date')
    inventorys = Inventory.objects.all().order_by('-created_date')
    context['orders'] = orders
    context['inventorys'] = inventorys
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'documents.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def select_documents(request):
    context = dict()
    orders = Order.objects.all()
    context['orders'] = orders
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'select_documents.html', context)
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
            if 'quantity' in data:
                if int(data['quantity']) < 0:
                    raise ValueError
                
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
        return JsonResponse({'status': 'error', 'message': "Malumotlarni to'ldirishda xatolik"})


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
    context['products'] = list(Product.objects.filter(count__gt=0).order_by('name'))         
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
    context['products'] = list(Product.objects.all().order_by('name'))
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
    refresh_count_for_products()
    drivers_list = list(Driver.objects.all().order_by('name'))

    drivers = []
    for driver in  drivers_list:
        cash = 0
        for payment in Payment.objects.filter(driver=driver):
            cash -= payment.cash
        for order in Order.objects.filter(driver=driver):
            order_cash = order.cash
            for refund in Refund.objects.filter(order=order):
                for refund_product in refund.Refund.all():
                    order_cash -= refund_product.product.case * refund_product.count * refund_product.price
            cash += order_cash
        drivers.append(
            {
                'id': driver.id,
                'photo': driver.photo,
                'name': driver.name,
                'phone': driver.phone,
                'auto': driver.auto,
                'cash': cash
            }
        )
    context = {
        'id': 1,
        'drivers': drivers,
    }
    
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
    context['products'] = list(Product.objects.filter(count__gt=0).order_by('name'))
    context['driver'] = driver
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'driver.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    

""" @login_required
def finance(request):
    
    orders_all = Order.objects.all().order_by('-created_date')
    orders_1 = Order.objects.filter(status='Yakunlandi').order_by('-created_date')
    orders_2 = Order.objects.filter(status='Jarayonda').order_by('-created_date')
    context = dict()
    context['orders_all'] = orders_all
    context['orders_1'] = orders_1
    context['orders_2'] = orders_2
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.") """

@login_required
def finance_driver(request):
    refresh_count_for_products()
    drivers_list = list(Driver.objects.all())
    total_cash = 0
    drivers = []
    for driver in  drivers_list:
        cash = 0
        for order in Order.objects.filter(driver=driver):
            order_cash = order.cash
            for refund in Refund.objects.filter(order=order):
                for refund_product in refund.Refund.all():
                    order_cash -= refund_product.product.case * refund_product.count * refund_product.price
            cash += order_cash
        for payment in Payment.objects.filter(driver=driver):
            cash -= payment.cash
        drivers.append(
            {
                'id': driver.id,
                'photo': driver.photo,
                'name': driver.name,
                'phone': driver.phone,
                'auto': driver.auto,
                'cash': cash
            }
        )
        total_cash += cash
    context = {
        'id': 1,
        'drivers': drivers,
        'total_cash': total_cash
    }
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance-driver.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

""" @login_required
def order_detail(request, id=1):
    context = dict()
    order = Order.objects.get(id=id)
    payments = Payment.objects.filter(order=order)
    refunds = Refund.objects.filter(order=order)
    refund_products = []
    total_cash = 0
    for refund in refunds:
        for refund_product in refund.Refund.all():
            refund_products.append(
                {
                    'id': refund_product.id,
                    'name': refund_product.product.name,
                    'product': refund_product.product,
                    'refund': refund_product.refund,
                    'price': refund_product.price,
                    'count': refund_product.count,
                    'cash': refund_product.product.case * refund_product.count * refund_product.price,
                }
            )
            total_cash += refund_product.product.case * refund_product.count * refund_product.price
    order_products = OrderProduct.objects.filter(order=order)
    context['refund_products'] = refund_products
    context['order_products'] = order_products
    context['total_cash'] = total_cash
    context['order'] = order
    context['payments'] = payments
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'order_detail.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.") """

@login_required
def finance_driver_detail(request, id=1):
    context = dict()
    driver = Driver.objects.get(id=id)
    orders = Order.objects.all()
    payments = Payment.objects.filter(driver=driver)

    cash = 0
    for order in Order.objects.filter(driver=driver):
        order_cash = order.cash
        """ for refund in Refund.objects.filter(order=order):
            for refund_product in refund.Refund.all():
                order_cash -= refund_product.product.case * refund_product.count * refund_product.price """
        cash += order_cash
    """ for payment in Payment.objects.filter(driver=driver):
        cash -= payment.cash """
    context['driver'] = {
            'driver':driver,
            'id': driver.id,
            'photo': driver.photo,
            'name': driver.name,
            'phone': driver.phone,
            'auto': driver.auto,
            'cash': cash
    }
    

    orders = Order.objects.filter(driver=driver)
    context['payments'] = payments
    context['orders'] = orders
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance-driver-detail.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
