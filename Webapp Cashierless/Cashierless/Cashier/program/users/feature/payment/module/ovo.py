import requests as req, json
from random import randint
import os.path

class OVO:
    def __init__(self):
        self.headers = {
            "Content-Encoding": "gzip, deflate",
            "App-Version": "3.6.0",
            "Content-Type": "application/json, charset=UTF-8",
            "Host": "api.ovo.id",
            "User-Agent": "okhttp/3.11.0"
        }

    def sendRequest(self, nomorOvo):
        deviceId = str(str(randint(111,999)) + 'ff' + str(randint(111,999)) + '-b7fc-3b' + str(randint(11,99)) + '-b' + str(randint(11,99)) + 'd-' + str(randint(1111,9999)) + 'd2fea8e5')
        url = "https://api.ovo.id/v1.1/api/auth/customer/login2FA"
        payload = {
            "deviceId":deviceId,
            "mobile":nomorOvo
        }

        r = req.post(url=url, headers=self.headers, data=json.dumps(payload))

        balik = deviceId
        if not r.status_code == 200:
            balik = "Error! Tolong update script anda :D"

        return balik

    def konfirmasiCode(self, deviceId, nomorOvo, verificationCode):
        url = "https://api.ovo.id/v1.1/api/auth/customer/login2FA/verify"
        payload = {
            "deviceId":deviceId,
            "mobile": nomorOvo,
            "verificationCode": verificationCode
        }
        r = req.post(url=url, headers=self.headers, data=json.dumps(payload))

        balik = "Anda berhasil Login!, Silahkan konfirmasi security code anda."
        if not r.status_code == 200:
            balik = "Harap periksa kode verifikasi anda"
        return balik

    def konfirmasiSecurityCode(self, deviceId, nomorOvo, securityCode):
        url = "https://api.ovo.id/v1.1/api/auth/customer/loginSecurityCode/verify"
        payload = {
            "mobile":nomorOvo,
            "securityCode":securityCode,
            "deviceUnixtime":1539175105,
            "appVersion":"3.14.0",
            "deviceId":deviceId,
            "macAddress":"08:62:66:67:81:39",
            "osName":"android",
            "osVersion":"5.0",
            "pushNotificationId":"FCM|e1-j8yB55QI:APA91bFan4mLCWogE4ols2OFSmz1YjgB71tKwZA0Y-IkwJSiKzG1ALJ6oxGuSQLYXLQWG8dujmdeWOdPn-gWWc_0fDcaO8BaPeZQbiF9wd3pfFU1NcYv54CUU80yPAZMS0nbNqfgHosJ"
        }

        r = req.post(url=url, headers=self.headers, data=json.dumps(payload))

        balik = ['Token: ']
        if r.status_code == 200:
            o = open(f"{nomorOvo} - OVO.txt", 'w')
            o.write(json.loads(json.dumps(r.json()))['token'])
            o.close()

            balik.append(json.loads(json.dumps(r.json()))['token'])
        else:
            balik[0] = "Security Code anda salah, Mohon coba lagi!"

        balik = "".join(balik)
        return balik

    def checkMutation(self, nomorOvo, limit = 10):
        url = f"https://api.ovo.id/wallet/v2/transaction?page=1&limit={limit}&productType=001"
        headers = self.headers
        dir_path = os.path.dirname(os.path.realpath(__file__))
        headers['Authorization'] = open(os.path.join(dir_path, f"{nomorOvo} - OVO.txt"), 'r').read()

        r = req.get(url=url, headers=headers)
        var = {}
        print(r.status_code)
        if r.status_code == 200:
            var['hasil'] = r.json()
        else:
            var['hasil'] = "Error"
        return var['hasil']


# ovo = OVO()
# gojek = GOJEK()
# nomorHP = "081338634040"
# deviceId = "264ff997-b7fc-3b35-b18d-9465d2fea8e5"
# loginToken = "ceb1ad35-f132-41ac-b682-462606877890"

# print(ovo.sendRequest(nomorHP))
# print(ovo.konfirmasiCode(deviceId, nomorHP, "3363"))
# print(ovo.konfirmasiSecurityCode(deviceId, nomorHP, "973173"))
# print(ovo.checkMutation(nomorHP))

# print(gojek.sendRequest(nomorHP))
# print(gojek.konfirmasiCode(loginToken, nomorHP, "6279"))
# print(gojek.checkMutation(nomorHP))