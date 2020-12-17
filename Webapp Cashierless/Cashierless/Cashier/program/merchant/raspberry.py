from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ... import models as db

from pytz import timezone
import datetime, json

currentDate = datetime.datetime.now()

def merchant_auth(request, method):
    merchant = db.Merchant.objects.filter(access_key = request.headers.get('key'))
    
    respond = {
        "status": False,
        "message": f"This Restful API access only support HTTP {method} Method only!" if not request.method == method else "Your access key is not valid to access this Restful API Access"
    }
    
    if merchant.exists():
        respond['data'] = {
            "merchant": merchant[0].name,
        }
     
    return merchant, respond, method

def get_enter_status(request):
    merchant, respond, method = merchant_auth(request, 'GET')
    if not merchant.exists() or not request.method == method:
        return JsonResponse(respond, safe=False)
    
    cekRemaining = db.RemainingCustomer.objects.filter(merchants = merchant[0]).order_by('-id')
    if not cekRemaining.exists():
        respond['message'] = "Hmm.. seem's your system is not working properly"
        return JsonResponse(respond, safe=False)
    
    respond['data']["is_enter"] = cekRemaining[:1][0].is_enter
    respond['data']["remaining_id"] = cekRemaining[:1][0].id
    
    respond['status'] = True
    del respond['message']
    
    return JsonResponse(respond, safe=False)

@csrf_exempt
def update_enter_status(request):
    merchant, respond, method = merchant_auth(request, 'PUT')
    if not merchant.exists() or not request.method == method:
        return JsonResponse(respond, safe=False)
    
    body = {}
    try:
        body = json.loads(request.body)
        db.RemainingCustomer.objects.filter(id = int(body['remaining_id'])).update(is_enter = True)
    except:
        respond['message'] = "Valid JSON body is required for this operation."
        return JsonResponse(respond, safe=False)
    
    del respond['message']
    respond['status'] = True
    
    return JsonResponse(respond, safe=False)

def get_last_transaction(request):
    merchant, respond, method = merchant_auth(request, 'GET')
    if not merchant.exists() or not request.method == method:
        return JsonResponse(respond, safe=False)
    
    cekTrx = db.Transaction.objects.filter(merchants = merchant[0]).order_by('-id')
    if not cekTrx.exists():
        respond['message'] = "Hmm.. seem's your system is not working properly"
        return JsonResponse(respond, safe=False)
    
    respond['data']["is_paid"] = cekTrx[:1][0].is_paid
    respond['data']["is_success"] = cekTrx[:1][0].is_success
    respond['data']["transaction_id"] = cekTrx[:1][0].id
    
    respond['status'] = True
    del respond['message']
    
    return JsonResponse(respond, safe=False)

@csrf_exempt
def update_exit_status(request):
    merchant, respond, method = merchant_auth(request, 'PUT')
    if not merchant.exists() or not request.method == method:
        return JsonResponse(respond, safe=False)
    
    try:
        body = json.loads(request.body)
        trxQ = db.Transaction.objects.filter(id = int(body['transaction_id']))
        
        if trxQ[0].is_paid:
            trxQ.update(is_success = True)
            
    except:
        respond['message'] = "Valid JSON body is required for this operation."
        return JsonResponse(respond, safe=False)
    
    respond['status'] = trxQ[0].is_paid
    del respond['message']
    
    return JsonResponse(respond, safe=False)