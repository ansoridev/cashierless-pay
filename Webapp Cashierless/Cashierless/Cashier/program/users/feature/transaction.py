from django.shortcuts import render, redirect
from .... import models as db
from . import home

def main_controller(request):
    return views(request) if request.session.get('email', '') else redirect('/signin/')

def detail_controller(request, trx_id):
    return detail(request, trx_id) if request.session.get('email', '') else redirect('/signin/')

def views(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    trx = db.Transaction.objects.filter(users__in=acc).order_by('-id')
    
    context = {
        "acc": acc[0],
        "trx": home.get_full_trx(trx)
    }
    
    return render(request, 'transaction.html', context)

def detail(request, trx_id):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    trx = db.Transaction.objects.filter(id=trx_id, users__in = acc)
    
    context = {
        "acc": acc[0],
        "trx": home.get_full_trx(trx)
    }
    
    return render(request, 'detail_transaction.html', context)