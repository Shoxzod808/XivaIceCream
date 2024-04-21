from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    print(request.user.groups)
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'index-1.html')
    # Проверяем, принадлежит ли пользователь к группе "Менеджер"
    elif request.user.groups.filter(name='Менеджер').exists():
        return render(request, 'index-2.html')
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
