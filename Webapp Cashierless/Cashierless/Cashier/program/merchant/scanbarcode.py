from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import raspberry
from pytz import timezone
import datetime, json, uuid
from ... import models as db

currentDate = datetime.datetime.now()

@csrf_exempt
def scan_barcode(request):
    merchant, respond, method = raspberry.merchant_auth(request, 'POST')
    if not merchant.exists() or not request.method == method:
        return JsonResponse(respond, safe=False)
    
    try:
        body = json.loads(request.body)
        cekBarcodeItem = db.ItemBarcode.objects.filter(barcode = body['barcode'], is_used = False)
    except:
        respond['message'] = "Valid JSON body is required for this operation."
        return JsonResponse(respond, safe=False)
    
    if not cekBarcodeItem.exists():
        respond['message'] = "Barcode is not registered!, Please re-scan the barcode."
        return JsonResponse(respond, safe=False)
    
    cekItem = db.Item.objects.filter(id = cekBarcodeItem[:1][0].items.id)
    if cekItem[:1][0].stocks < 1:
        respond['message'] = "Items is currently out of stock"
        return JsonResponse(respond, safe=False)
        
    trx = db.Transaction.objects.filter(merchants = merchant[0]).order_by('-id')
    global payBarcode
    if trx.exists() and not trx[:1][0].is_paid:
        trx = trx[:1][0]
        payBarcode = db.MerchantBarcode.objects.get(transactions = trx)
    else:
        trx = db.Transaction(
            record = uuid.uuid4().hex[:8].upper(),
            merchants = merchant[0],
            total = 0,
            time = currentDate.replace(tzinfo=timezone('Asia/Jakarta')),
        )
        trx.save()
        payBarcode = db.MerchantBarcode(
            merchants = merchant[0],
            barcode = uuid.uuid4().hex[:20].upper(),
            type = "PAY",
            transactions = trx
        )
        payBarcode.save()
    
        
    cekSubTrx = db.SubTransaction.objects.filter(items = cekBarcodeItem[:1][0].items, transactions = trx)
    if cekSubTrx.exists():
        cekSubTrx.update(quantity = cekSubTrx[:1][0].quantity + 1)
        subTrx = cekSubTrx[:1][0]
    else:
        cekSubTrx = db.SubTransaction(
            transactions = trx,
            items = cekBarcodeItem[:1][0].items,
            quantity = 1
        )
        cekSubTrx.save()
        subTrx = cekSubTrx
    
    db.Transaction.objects.filter(id = trx.id).update(total = trx.total + cekBarcodeItem[:1][0].items.price)
    cekItem.update(stocks = cekItem[:1][0].stocks - 1)
    
    respond['data']['record'] = trx.record
    respond['data']['pay_barcode'] = payBarcode.barcode
    respond['data']['item'] = cekBarcodeItem[:1][0].items.name
    respond['data']['item_quantity'] = int(subTrx.quantity)
    respond['data']['item_unit'] = cekBarcodeItem[:1][0].items.unit
    respond['data']['item_price'] = int(cekBarcodeItem[:1][0].items.price)
    respond['data']['total'] = int(trx.total + cekBarcodeItem[:1][0].items.price)
    
    cekBarcodeItem.update(is_used = True)
    del respond['message']
    respond['status'] = True
    
    return JsonResponse(respond, safe=False)
    