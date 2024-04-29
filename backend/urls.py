from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import login_view, index, logout_view, kirim, document, documents, process_payment, finance_driver, finance_driver_detail
from .views import chiqim, save_products, driver, process_products, select_documents, save_table_data

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', index, name='home'),
    path('chiqim', chiqim, name='chiqim'),
    path('driver-<int:id>', driver, name='driver'),
    path('kirim', kirim, name='kirim'),
    #path('finance', finance, name='finance'),
    path('finance-driver', finance_driver, name='finance_driver'),
    path('finance-driver-detail/<int:id>', finance_driver_detail, name='finance_driver_detail'),
    #path('order/<int:id>', order_detail, name='order_detail'),
    path('logout/', logout_view, name='logout'),
    path('document/<int:id>/', document, name='document'),
    #path('documents', documents, name='documents'),
    #path('select_documents', select_documents, name='select_documents'),
    path('save-products/', save_products, name='save_products'),
    path('process-products/', process_products, name='process_products'),
    path('process-payment/', process_payment, name='process_payment'),
    path('save-table-data/', save_table_data, name='save_table_data'),
]



# Настройте обработку статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
