from django.shortcuts import render, redirect
from .... import models as db

def controller(request):
    return views(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def views(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    checkSession(acc)
    
    trx = db.Transaction.objects.filter(merchants__in=acc).exclude(is_paid=False).order_by('-id')[:7]
    
    context = {
        "acc": acc[0],
        "trx": get_full_trx(trx)
    }
    return render(request, 'merchant_home.html', context)

def get_full_trx(trx):
    trx_list = []
    
    for trx_loop in trx:
        trx_sub = db.SubTransaction.objects.filter(transactions=trx_loop)
        trx_json = {
            "id": trx_loop.id,
            "record": trx_loop.record,
            "time": trx_loop.time,
            "total": trx_loop.total,
            "is_success": trx_loop.is_success
        }
        if trx_loop.users:
            trx_json['users'] = trx_loop.users.name
            trx_json['users_email'] = trx_loop.users.email
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
        del request.session['merchant']
        return redirect('/merchant/signin/')
    
def logout(request):
    del request.session['merchant']
    return redirect('/merchant/signin/')

def log_entry(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    checkSession(acc)
    
    context = {
        "acc": acc[0],
        "log": db.RemainingCustomer.objects.filter(merchants__in = acc)
    }
    
    return render(request, 'merchant_log_entry.html', context)