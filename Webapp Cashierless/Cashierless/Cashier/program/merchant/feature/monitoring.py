from django.shortcuts import render, redirect
from .... import models as db
from . import home

def controller(request):
    return views(request) if request.session.get('merchant', '') or request.GET.get('key', '') else redirect('/merchant/signin/')

def barcode_controller(request):
    return load_barcode(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def item_controller(request):
    return load_item(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def views(request):
    if request.GET.get('key', ''):
        key = request.GET.get('key', '')
        query = db.Merchant.objects.filter(access_key=key)
        if query.exists():
            request.session['merchant'] = key
        else:
            return redirect('/merchant/signin/')
        
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
        
    context = {
        "acc": acc[0],
    }
    
    return render(request, 'merchant_monitoring.html', context)

def load_barcode(request):
    barcode = db.MerchantBarcode.objects.filter(type="PAY", merchants__access_key=request.session.get('merchant', ''))
    if barcode.exists():
        total = barcode[:1][0].transactions.total
        barcode = barcode[:1][0].barcode
    else:
        barcode = ''
        total = 0
    return render(request, 'barcode_pay.html', context={ 'barcode': barcode, 'total': total })

def load_item(request):
    itemQ = db.Transaction.objects.filter(is_success=False, is_paid=False, merchants__access_key=request.session.get('merchant', ''))[:1]
    items = home.get_full_trx(itemQ)[0]['summary'] if itemQ.exists() else ''
    context = {
        'itemQ': True if itemQ.exists() else False,
        'items': items
    }
    return render(request, 'item_monitoring.html', context=context)