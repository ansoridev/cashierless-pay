# Cashierless Pay

[![N|Solid](https://cashierlesspay.com/static/assets/images/cashierless_full.png)](https://cashierlesspay.com/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/ansoridev/cashierless-pay)

Perkenalkan project kami Cashierless Pay, yaitu Project untuk menggantikan kasir konvensional di Toko menjadi Toko tanpa kasir, yang telah di optimasi dan di integrasikan dengan sistem yang dapat mencegah pencurian. 
Cashierless ini juga dapat membantu mencegah penyebaran virus corona - 19 yang jika pada kasir konvensional yang harus bertatap muka dan dapat menyebabkan cluster penularan Virus COVID-19.
Pada Cashierless ini sendiri menggunakan teknologi antara lain:

- Web Teknologi: 
      Django (Python)
      Django ASGI Web Sockets
      Vannila JS
- IoT Teknologi:
      Raspberry PI 3 (Pemrograman menggunakan Python)
      RFID Reader, RFID Anthenna, RFID Chip
      Selenoid door lock (Customize)
      Magnetic sensor door lock

Pada project Cashierless ini sendiri berkonsepkan Project Start-Up dikarenakan menggunakan konsep Multi Merchant, serta multi pengguna.
dan sudah dilengkapi dengan integrasi ke Payment Gateway, untuk top up secara otomatis.

Terima kasih kepada:
- SMK Negeri 3 Metro
- Pusat Prestasi Nasional
- Kamp Kreatif SMK Indonesia
- GunaPedia.co.id Hosting & Domain

> Setidaknya walaupun kami bukan juara
> namun kami yakin, projek kami berguna untuk masyarakat
> serta menggembangkan inovasi dalam hal teknologi
> yang dapat mampu memajukan indonesia kedepannya
> karena masa depan bangsa ada ditangan kita.

### Tim Cashierless Pay

- Ahmad Ansori - XI RPL
- Michael Jullius - XI RPL
- Nosa Rahmanda - X RPL
- Aulia Rahmadani - X RPL
- Fitroh Laila M - X RPL

### Installation

Anda dapat mengaktifkan project webapp dengan membuat environment terpisah untuk project ini dengan cara

Untuk Windows
```
> python3 -m venv venv
> "venv/Scripts/activate"
> pip install -r requirement.txt
```

Untuk Linux
```
$ python3 -m venv venv
$ source "venv/bin/activate"
$ pip install -r requirement.txt
```

Setelah itu anda dapat menyesuaikan database sesuai dengan konfigurasi keinginan anda
dan lakukan migrasi database dengan cara
```
> cd Cashierless
> py m migrate
> py m makemigrations Cashier
> py m migrate Cashier
```

Lalu lakukan pengaktifan server Django
```
> python3 m runserver 0.0.0.0:80 --insecure
```

dan untuk membuat akun untuk administrator yang berada di path /admin
```
> python3 m createsuperuser
```

### Terima Kasih
