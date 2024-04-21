from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import login_view, index, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', index, name='home'),
    path('chiqim', index, name='chiqim'),
    path('kirim', index, name='kirim'),
    path('logout/', logout_view, name='logout'),
]



# Настройте обработку статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
