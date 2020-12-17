"""Cashierless URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect, render
from django.conf.urls import include

from .program.users.auth import signin, signup
from .program.users.feature import home, transaction, addfunds, scanqr
from .program.merchant import raspberry, scanbarcode
from .program.merchant.auth import signin as signin_merchant
from .program.merchant.feature import home as home_merchant, transaction as transaction_merchant, monitoring, item

from datetime import datetime

def index(request):
    return redirect('/home/')
def index_merchant(request):
    return redirect('/merchant/home/')
def qr_show(request, barcode):
    return render(request, 'qr_show.html', context={ 'barcode': barcode }, content_type="image/svg+xml")

def on_off_theft(request, id):
    from .models import RemainingCustomer
    
    trxfil = RemainingCustomer.objects.filter(id = id)
    trxfil.update(
        is_theft = True if not trxfil[0].is_theft else False
    )
    
    return redirect('/admin/Cashier/transaction/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('signin/', signin.controller),
    path('signup/', signup.controller),
    path('home/', home.controller),
    path('logout/', home.logout),
    path('transaction/', transaction.main_controller),
    path('transaction/<int:trx_id>/', transaction.detail_controller),
    path('topup/', addfunds.main_controller),
    path('topup/history/', addfunds.history_controller),
    path('log/merchant/', home.log_entry),
    path('on-off-theft/<int:id>/', on_off_theft),
    path('topup/<int:id>/', addfunds.detail_controller),
    path('scanbarcode/', scanqr.controller),
    path('scanbarcode/validate/', scanqr.ajax_controller),
    path('api/get/enter-status', raspberry.get_enter_status),
    path('api/put/enter-status', raspberry.update_enter_status),
    path('api/get/last-transaction', raspberry.get_last_transaction),
    path('api/post/scan-barcode', scanbarcode.scan_barcode),
    path('api/put/exit-status', raspberry.update_exit_status),
    path('qr_show/<str:barcode>/', qr_show),
    path('qr_render/', include('qr_code.urls', namespace="qr_code")),
    path('merchant/', index_merchant), path('merchant', index_merchant),
    path('merchant/signin/', signin_merchant.controller),
    path('merchant/home/', home_merchant.controller),
    path('merchant/logout/', home_merchant.logout),
    path('merchant/monitoring/', monitoring.controller),
    path('merchant/monitoring/pay/', monitoring.barcode_controller),
    path('merchant/monitoring/item/', monitoring.item_controller),
    path('merchant/transaction/', transaction_merchant.main_controller),
    path('merchant/transaction/<int:trx_id>/', transaction_merchant.detail_controller),
    path('merchant/log/', home_merchant.log_entry),
    path('merchant/item/', item.main_management_controller),
    path('merchant/item/QR/', item.qr_management_controller)
    # path('merchant/withdraw/'),
    # path('merchant/withdraw/history/'),
    # path('merchant/withdraw/history/<int:id>/')
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
