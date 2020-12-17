from django.shortcuts import render, redirect
from .... import models as db
from . import home

def main_controller(request):
    return views(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def detail_controller(request, trx_id):
    return detail(request, trx_id) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def views(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
    
    trx = db.Transaction.objects.filter(merchants__in=acc, is_paid=True).order_by('-id')
    
    context = {
        "acc": acc[0],
        "trx": home.get_full_trx(trx)
    }
    
    return render(request, 'merchant_transaction.html', context)

def detail(request, trx_id):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
    
    trx = db.Transaction.objects.filter(id=trx_id)
    
    context = {
        "acc": acc[0],
        "trx": home.get_full_trx(trx)
    }
    
    return render(request, 'merchant_detail_transaction.html', context)