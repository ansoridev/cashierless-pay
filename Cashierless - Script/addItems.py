import cv2, requests, json, humanize, time

cap = cv2.VideoCapture(0)
settings = json.loads(open("settings.json", "r").read())["settings"]
errlist = []
errlist.append('')

while True:
    try:
        _, img = cap.read()
        detector = cv2.QRCodeDetector()
        barcode, bbox, _ = detector.detectAndDecode(img)
    except:
        bbox = None
    
    if(bbox is not None):
        try:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 255), thickness=2)
            cv2.putText(img, barcode, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
        except:
            barcode = ''
            
        # cv2.imshow("code detector", img)
            
        if barcode and not barcode in errlist:
            print("Processing barcode...")
            errlist[0] = barcode
            data = json.dumps({ "barcode": barcode.replace('\r', '') })
            req = requests.post(
                url = settings['api_route'] + '/api/post/scan-barcode',
                data = data,
                headers = {
                    "content-type": "application/json",
                    "key": settings['api_key']
                }
            )
            respond = json.loads(json.dumps(req.json()))
            print(data)
            if not respond['status']:
                print(respond['message'])
            else:
                print(f"Item has been added to transaction #{respond['data']['record']}")
                print(f"Item Name: {respond['data']['item']}")
                print(f"Item Quantity: {respond['data']['item_quantity']}/{respond['data']['item_unit']}")
                print(f"Item Price: Rp. {humanize.intcomma(respond['data']['item_price'])}")
                print(f"Total Transaction: Rp. {humanize.intcomma(respond['data']['total'])}")
                print(f"Payment Barcode: {respond['data']['pay_barcode']}")
    if(cv2.waitKey(1) == ord("q")):
        break

