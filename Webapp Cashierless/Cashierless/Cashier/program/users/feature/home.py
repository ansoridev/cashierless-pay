from django.shortcuts import render, redirect
from .... import models as db

def controller(request):
    return views(request) if request.session.get('email', '') else redirect('/signin/')

def views(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    checkSession(acc)
    
    trx = db.Transaction.objects.filter(users__in=acc).exclude(is_paid=False).order_by('-id')[:7]
    
    context = {
        "acc": acc[0],
        "trx": get_full_trx(trx),
        "paymentoto": db.PaymentMethod.objects.filter(type="OTOMATIS"),
        "paymentman": db.PaymentMethod.objects.filter(type="MANUAL")
    }
    return render(request, 'home.html', context)

def get_full_trx(trx):
    trx_list = []
    
    for trx_loop in trx:
        trx_sub = db.SubTransaction.objects.filter(transactions=trx_loop)
        trx_json = {
            "id": trx_loop.id,
            "record": trx_loop.record,
            "merchants": trx_loop.merchants.name,
            "merchants_location": trx_loop.merchants.location,
            "time": trx_loop.time,
            "total": trx_loop.total,
            "is_success": trx_loop.is_success
        }
        sub_trx_list = []
        for trx_sub_loop in trx_sub:
            trx_sub_json = {
                "items_name": trx_sub_loop.items.name,
                "items_unit": trx_sub_loop.items.unit,
                "items_price": trx_sub_loop.items.price,
                "items_image": trx_sub_loop.items.image,
                "quantity": trx_sub_loop.quantity,
                "items_totals": trx_sub_loop.items.price * trx_sub_loop.quantity
            }
            sub_trx_list.append(trx_sub_json)
        trx_json['summary'] = sub_trx_list
        trx_list.append(trx_json)
        
    return trx_list

def checkSession(acc):
    if not acc:
        del request.session['email']
        return redirect('/signin/')
    
def logout(request):
    del request.session['email']
    return redirect('/signin/')

def log_entry(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    checkSession(acc)
    
    context = {
        "acc": acc[0],
        "log": db.RemainingCustomer.objects.filter(users__in = acc)
    }
    
    return render(request, 'log_entry.html', context)