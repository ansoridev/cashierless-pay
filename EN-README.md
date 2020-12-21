# Cashierless Pay

[![N|Solid](https://cashierlesspay.com/static/assets/images/cashierless_full.png)](https://cashierlesspay.com/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/ansoridev/cashierless-pay)

Introduce our project Cashierless Pay, which is a project to replace conventional cashiers in shops to shop without cashiers, which have been optimized and integrated with a system that can prevent theft.
Cashierless can also help prevent the spread of the corona - 19 virus, which, if at a conventional cashier, must meet face to face and can cause clusters of COVID-19 virus transmission.
Cashierless uses technology, including:

- Web Technology:
      Django (Python)
      Django ASGI Web Sockets
      Vannila JS
- IoT Technology:
      Raspberry PI 3 (Programming using Python)
      RFID Reader, RFID Anthenna, RFID Chip
      Selenoid door lock (Customize)
      Magnetic sensor door lock

The Cashierless project itself has a Start-Up Project concept because it uses the Multi Merchant concept, as well as multi-users.
and is equipped with integration to the Payment Gateway, for top up automatically.

Thanks to:
- SMK Negeri 3 Metro
- National Achievement Center
- Indonesian Vocational High School Creative Camp
- GunaPedia.co.id Hosting & Domain

> At least even if we're not champions
> but we believe, our project is useful for the community
> as well as developing innovations in technology
> which can advance Indonesia in the future
> because the future of the nation is in our hands.

### Cashierless Pay Team

- Ahmad Ansori - XI RPL
- Michael Jullius - XI RPL
- Nosa Rahmanda - X RPL
- Aulia Rahmadani - X RPL
- Fitroh Laila M - X RPL

### Installation

You can activate the webapp project by creating a separate environment for this project in a

For Windows
```
> python3 -m venv venv
> "venv / Scripts / activate"
> pip install -r requirement.txt
```

For Linux
```
$ python3 -m venv venv
$ source "venv / bin / activate"
$ pip install -r requirement.txt
```

After that you can customize the database according to your desired configuration
and do database migration in a way
```
> Cashierless cd
> py m migrate
> py m cashier makemigrations
> py m cashier migrate
```

Then do the Django server activation
```
> python3 m runserver 0.0.0.0:80 --insecure
```

and to create an account for an administrator who is in the path / admin
```
> python3 m createsuperuser
```

### Thank you
