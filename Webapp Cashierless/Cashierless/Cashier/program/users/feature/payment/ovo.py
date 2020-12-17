from .module.ovo import OVO

def byNominal(phone, nominal):
    ovo = OVO()
    ovo = ovo.checkMutation(phone)
    print(ovo)
    hasil = {"status": False}
    if not ovo == "Error":
        for i in ovo['data'][0]['complete']:
            if i['emoney_topup'] == int(nominal):
                hasil['status'] = True
                hasil['ref'] = i['merchant_invoice']
                hasil['date'] = i['transaction_date'] + ' ' + i['transaction_time']
                hasil['from'] = i['desc3']
    return hasil