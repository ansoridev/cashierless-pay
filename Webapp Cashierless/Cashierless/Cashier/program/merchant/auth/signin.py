from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .... import models as db
import json

def controller(request):
    return redirect('/merchant/home/') if request.session.get('merchant', '') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    return render(request, 'auth/merchant_signin.html')

def ajax(request):
    result = {
        "status": False
    }
    
    if request.is_ajax():
        key = request.POST.get('key', '')
        query = db.Merchant.objects.filter(access_key=key)
        if query.exists():
            result['status'] = True
            request.session['merchant'] = key
                
    return JsonResponse(result)