from django.shortcuts import render, redirect
from django.http import JsonResponse
from .... import models as db
from . import home

def main_management_controller(request):
    return main_management(request) if not request.method == 'POST' else ajax_management(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def qr_management_controller(request):
    return qr_management(request) if request.session.get('merchant', '') else redirect('/merchant/signin/')

def main_management(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
    
    item = db.Item.objects.filter(merchants__in=acc).order_by('-id')
    
    context = {
        "acc": acc[0],
        "item": item
    }
    
    return render(request, 'item_management.html', context)

def qr_management(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
    
    item = db.ItemBarcode.objects.filter(items__merchants__in = acc).order_by('-id')
    
    context = {
        "acc": acc[0],
        "item": item
    }
    
    return render(request, 'qr_management.html', context)

def ajax_management(request):
    acc = db.Merchant.objects.filter(access_key=request.session.get('merchant', ''))
    home.checkSession(acc)
    
    id = request.POST.get('id', '')
    tipe = request.POST.get('type', '')
    name = request.POST.get('name', '')
    unit = request.POST.get('unit', '')
    stocks = int(request.POST.get('stocks', ''))
    price = int(request.POST.get('price', '').replace('Rp. ', ''))
    
    result = {
        "status": False
    }
    
    if tipe == "add":
        db.Item(
            name = name,
            unit = unit,
            price = price,
            stocks = stocks,
            merchants = acc[0]
        ).save()
        result['status'] = True
        result['message'] = f"Item of {name} has been added to the merchant."
        return JsonResponse(result, safe=False)
    
    ItemQuery = db.Item.objects.filter(id = id, merchants__in = acc)
    
    if not ItemQuery:
        result['message'] = "The selected item ID is not registered in our system"
        return JsonResponse(result, safe=False)
            
    if tipe == "update":
        ItemQuery.update(
            name = name,
            unit = unit,
            price = price,
            stocks = stocks
        )
        result['status'] = True
        result['message'] = f"Item of {name} has been updated with latest data."
    elif tipe == "delete":
        ItemQuery.delete()
        result['status'] = True
        result['message'] = f"Item of {name} has been deleted!."
        
    return JsonResponse(result, safe=False)