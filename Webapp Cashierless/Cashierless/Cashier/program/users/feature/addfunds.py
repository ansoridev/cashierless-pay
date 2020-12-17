from django.shortcuts import render, redirect
from django.http import JsonResponse
from .... import models as db
from . import home
import uuid
from random import randint

def main_controller(request):
    return views(request) if not request.method == 'POST' else ajax_addfunds(request) if request.session.get('email', '') else redirect('/signin/')

def detail_controller(request, id):
    return detail(request, id) if not request.method == 'POST' else ajax_confirmpay(request, id) if request.session.get('email', '') else redirect('/signin/')

def history_controller(request):
    return history(request) if request.session.get('email', '') else redirect('/signin/')

def views(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    context = {
        "acc": acc[0],
        "paymentoto": db.PaymentMethod.objects.filter(type="OTOMATIS"),
        "paymentman": db.PaymentMethod.objects.filter(type="MANUAL")
    }
    return render(request, 'addfunds.html', context=context)

def detail(request, id):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    deposit = db.TopUpHistory.objects.filter(id = id, users__in = acc)
    
    if not deposit:
        return redirect('/home/topup/history/')
    
    totalbayar = deposit[0].codeunik + deposit[0].total  if deposit[0].method.type == "OTOMATIS" else 0 + deposit[0].total 
    
    context = {
        "deposit": deposit[0],
        "totalbayar": totalbayar
    }
    
    return render(request, 'detail_addfunds.html', context)

def history(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    deposit = db.TopUpHistory.objects.filter(users__in=acc).order_by('-id')
    
    context = {
        "acc": acc[0],
        "deposit": deposit
    }
    
    return render(request, 'addfunds_history.html', context)

def ajax_confirmpay(request, id):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    pay = db.TopUpHistory.objects.filter(id=id, users__in = acc)
    
    result = {
        "status": False
    }
    
    if request.POST.get('type', '') == "CANCEL":
        pay.update(status="CANCELED")
        result['status'] = True
        result['message'] = "We have canceled your add funds transaction. Now you can make a new add funds"
        return JsonResponse(result, safe=False)
    
    from .payment import ovo
    
    if not pay:
        result['message'] = "Payment Method is invalid, Please don't distrubing system!'"
        return JsonResponse(result, safe=False)
    
    var = {
        "saldoawal": acc[0].balance,
        "total": pay[0].total,
        "received": pay[0].receive,
        "codeunik": pay[0].codeunik,
        "method": pay[0].method.name,
        "type": pay[0].method.type
    }

    var['total'] = var['received'] + var['codeunik']
    
    if var['type'] == "MANUAL":
        result['message'] = "You're not supposed to be able access this action, Please don't distrubing system!'"
        return JsonResponse(result, safe=False)
    
    if var['method'] == "OVO":
        cek = ovo.byNominal(pay[0].method.number, var['total'])
        if cek['status'] == False:
            result['message'] = "Payment not found"
            return JsonResponse(result, safe=False)
        
        pay.update(ref=cek['ref'], datepaid=cek['date'], frompaid=cek['from'], status="SUCCESS")
        var['saldo'] = int(var['saldoawal']) + int(var['received']) + int(var['codeunik'])
        acc.update(balance=var['saldo'])
        
        result['status'] = True
        result['message'] = "Thank you for making a payment, your balance has been added"
        
    return JsonResponse(result, safe=False)

def ajax_addfunds(request):
    acc = db.User.objects.get(email=request.session.get('email', ''))
    method = request.POST.get('method', '')
    amount = int(request.POST.get('amount', '').replace('Rp. ', ''))
    pay = db.PaymentMethod.objects.filter(id=int(method))
    topHist = db.TopUpHistory.objects.filter(users=acc).last()
    
    result = {
        "status": False
    }
    
    if amount < 10000:
        result['message'] = "Minimum add funds amount is Rp. 10.000, Please add more funds."
        return JsonResponse(result, safe=False)
    
    if not pay:
        result['message'] = "Payment Method is invalid, Please don't distrubing system!'"
        return JsonResponse(result, safe=False)
    
    if topHist:
        if topHist.status == "PENDING":
            result['message'] = "Please complete or cancel your last transaction before make other transaction."
            return JsonResponse(result, safe=False)
    
    var = {}
    var['codeunik'] = randint(111, 999)
    var['totalpay'] = int(amount)
    var['type'] = pay[0].type

    topupH = db.TopUpHistory(users=acc,record=uuid.uuid4().hex[:8].upper() , method=pay[0], total=amount,
                            receive=var['totalpay'], codeunik=var['codeunik'], status="PENDING")
    topupH.save()

    data = {}
    data['record'] = topupH.record
    data['id'] = topupH.id
    data['type'] = var['type']

    result['data'] = data
    result['status'] = True

    if var['type'] == "MANUAL":
        result['message'] = "You can make transaction then create ticket for confirm your transaction."
    else:
        result['message'] = "Let's complete your transaction, then it will automatically confirm!"
        
    return JsonResponse(result, safe=False)