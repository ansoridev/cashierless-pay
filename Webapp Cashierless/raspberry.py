import cv2, requests, json, gpiozero as io

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
settings = json.loads(open("settings.json", "r").read())["settings"]

while True:
    _, img = cap.read()
    barcode, bbox, _ = detector.detectAndDecode(img)
    
    if(bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 255), thickness=2)
        cv2.putText(img, barcode, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if barcode:
            print("Processing barcode...")
            req = requests.post(
                url = settings['api_route'] + '/api/post/scan-barcode',
                data = json.dumps({ "barcode": barcode }),
                headers = {
                    "content-type": "application/json",
                    "key": settings['api_key']
                }
            )
            respond = json.loads(json.dumps(req.json()))
            if not respond['status']:
                print(respond['message'])
            else:
                print(f"Item has been added to transaction #{respond['data']['record']}")
                print(f"Item Name: {respond['data']['item']}")
                print(f"Item Quantity: {respond['data']['item_quantity']}/{respond['data']['item_unit']}")
                print(f"Item Price: {respond['data']['item_price']}")
                print(f"Total Transaction: {respond['data']['total']}")
                print(f"Payment Barcode: {respond['data']['pay_barcode']}")
            
    if(cv2.waitKey(1) == ord("q")):
        break
