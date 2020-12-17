from django.shortcuts import render, redirect
from django.http import JsonResponse
from .... import models as db
from . import home

from pytz import timezone
import datetime, humanize

currentDate = datetime.datetime.now()

def controller(request):
    return views(request) if request.session.get('email', '') else redirect('/signin/')

def ajax_controller(request):
    return ajaxQr(request) if request.session.get('email', '') else redirect('/signin/')

def views(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
        
    context = {
        "acc": acc[0]
    }
    
    return render(request, 'scanqr.html', context=context)

def ajaxQr(request):
    acc = db.User.objects.filter(email=request.session.get('email', ''))
    home.checkSession(acc)
    
    respond = {
        "status": False,
        "message": "Your HTTP request is not an valid AJAX request."
    }
    
    if request.is_ajax():
        barcode = request.POST.get('barcode', '')
        qrcek = db.MerchantBarcode.objects.filter(barcode = barcode)
        if qrcek.exists():
            respond['data'] = {
                "type": qrcek[0].type,
                "merchant": qrcek[0].merchants.name
            }
            
            cekRemaining = db.RemainingCustomer.objects.filter(users = acc[0]).order_by('-id')
            cekTrx = db.Transaction.objects.filter(merchants = qrcek[0].merchants).order_by('-id')
                  
            if qrcek[0].type == "ENTER":
                def enterMerchant():
                    db.RemainingCustomer(
                        users = acc[0],
                        merchants = qrcek[0].merchants,
                        enterTime = currentDate.replace(tzinfo=timezone('Asia/Jakarta'))
                    ).save()
                    respond['status'] = True
                    respond['message'] = f"Welcome to {qrcek[0].merchants.name} 😄"
                
                if cekRemaining[:1].exists():
                    if not cekRemaining[:1][0].exitTime:
                        del respond['data']
                        respond['message'] = "You are already in the shop, so you cannot enter the shop!"
                    else:
                        enterMerchant()
                else:
                    enterMerchant()
            
            if qrcek[0].type == "EXIT":                
                def exitMerchant():
                    respond['message'] = "You cannot exit the store, because you not make an payment, at least make payment as guest"
                    exitTrx = db.Transaction.objects.filter(merchants = qrcek[0].merchants, is_paid = True, is_success = False).order_by('-id')
                    try:
                        def check_user(queryfilter, queryset):
                            hasil = ""
                            for qf in queryfilter:
                                print(str(qf))
                                if qf.users == queryset:
                                    hasil = qf.id
                            return hasil
                        
                        def update_exit(queryfilter, queryset):
                            hasil = ""
                            for qf in queryfilter:
                                if qf.users == queryset:
                                    queryfilter.update(is_success = True)
                            return hasil
                        
                        if cekRemaining[:1][0].is_theft:
                            respond['message'] = "We've detected that you're hiding items you haven't paid for. Please place the item in the place provided."
                            return JsonResponse(respond, safe=False)
                        
                        checkUsernya = check_user(exitTrx, acc[0])
                        if checkUsernya:
                            exitTrxs = db.Transaction.objects.get(id = checkUsernya)
                             
                            if not exitTrxs.is_success:
                                update_exit(exitTrx, acc[0])
                                
                        cekRemaining.update(exitTime = currentDate.replace(tzinfo=timezone('Asia/Jakarta')))
                        respond['status'] = True
                        respond['message'] = f"Thank you for shopping at {qrcek[0].merchants.name}, Have a nice day 🥳"
                    except:
                        print('Error code: EX291')

                if cekRemaining[:1].exists():
                    if cekRemaining[:1][0].exitTime:
                        del respond['data']
                        respond['message'] = "You have exit from the store, so you cannot exit again!"
                    else:
                        exitMerchant()
                else:
                    exitMerchant()
                    
            if qrcek[0].type == "PAY":
                respond['status'] = True
                respond['data']['total'] = qrcek[0].transactions.total
                if not request.POST.get('confirm', ''):   
                    respond['is_confirm'] = False
                    respond['message'] = f"Do you want to make a payment of Rp. {humanize.intcomma(int(qrcek[0].transactions.total))} at {qrcek[0].merchants.name}"                    
                    return JsonResponse(respond, safe=False)
                
                respond['is_confirm'] = True
                if acc[0].balance < qrcek[0].transactions.total:
                    respond['message'] = "Your balance is not sufficient to make a payment, let's fill in your balance"  
                    respond['data']['is_paid'] = False
                    return JsonResponse(respond, safe=False)
                    
                db.Transaction.objects.filter(id = qrcek[0].transactions.id).update(users = acc[0], is_paid = True)
                db.Merchant.objects.filter(id = qrcek[0].merchants.id).update(balance = qrcek[0].merchants.balance + qrcek[0].transactions.total)
                acc.update(balance = acc[0].balance - qrcek[0].transactions.total)
                itemQuery = db.Item.objects.filter(merchants = qrcek[0].merchants)
                for itemQ in itemQuery:
                    subTrxGet = db.SubTransaction.objects.filter(transactions = qrcek[0].transactions, items = itemQ)
                    if subTrxGet.exists():
                        db.Item.objects.filter(id = itemQ.id).update(stocks = itemQ.stocks - subTrxGet[:1][0].quantity)
                
                respond['data']['is_paid'] = True
                respond['message'] = f"Thank you for making purchases at {qrcek[0].merchants.name}"
                qrcek.delete()
                
        else:
            respond['message'] = "Barcode is not registered!, Please re-scan the barcode."
        
    return JsonResponse(respond, safe=False)