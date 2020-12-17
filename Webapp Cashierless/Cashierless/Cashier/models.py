from django.db import models
from pytz import timezone
import uuid, datetime

currentDate = datetime.datetime.now()
genTicket = uuid.uuid4().hex[:8].upper()
# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    foto = models.ImageField(upload_to = f"uploads/foto/{str(uuid.uuid4())}/", blank=False, null=False, default="/uploads/foto/default.png")
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return self.email
    
class Merchant(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    balance = models.IntegerField()
    access_key = models.CharField(max_length=255, default="default")
    
    def __str__(self):
        return self.name
    
class MerchantBarcode(models.Model):
    typeChoose = (
        ('ENTER', 'ENTER'),
        ('EXIT', 'EXIT'),
        ('PAY', 'PAY')
    )
    merchants = models.ForeignKey(to = Merchant, on_delete = models.CASCADE)
    barcode = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=typeChoose)
    transactions = models.ForeignKey(to = "Transaction", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.type 
    
class Transaction(models.Model):
    record = models.CharField(max_length=8)
    users = models.ForeignKey(to = "User", on_delete=models.CASCADE, blank=True, null=True)
    merchants = models.ForeignKey(to = "Merchant", on_delete=models.CASCADE)
    total = models.IntegerField()
    time = models.DateTimeField(default=currentDate.replace(tzinfo=timezone('Asia/Jakarta')))
    is_success = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.record
    
class Item(models.Model):
    units = (
        ('Pcs', 'Packages'),
        ('Ltr', 'Liter'),
        ('Kg', 'Kilogram')
    )
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, choices=units)
    price = models.IntegerField()
    merchants = models.ForeignKey(to = "Merchant", on_delete=models.CASCADE)
    stocks = models.IntegerField()
    image = models.ImageField(upload_to = f"uploads/items/{str(uuid.uuid4())}/", blank=False, null=False, default="/uploads/items/default.png")
    
    def __str__(self):
        return self.name
    
class ItemBarcode(models.Model):
    items = models.ForeignKey(to = Item, on_delete = models.CASCADE)
    barcode = models.CharField(max_length=500)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return self.items.name

class SubTransaction(models.Model):
    transactions = models.ForeignKey(to = "Transaction", on_delete=models.CASCADE)
    items = models.ForeignKey(to = "Item", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.items.name} - {self.quantity}/{self.items.unit}"
    
class RemainingCustomer(models.Model):
    users = models.ForeignKey(to = "User", on_delete=models.CASCADE)
    merchants = models.ForeignKey(to = "Merchant", on_delete=models.CASCADE)
    enterTime = models.DateTimeField(default=currentDate.replace(tzinfo=timezone('Asia/Jakarta')))
    exitTime = models.DateTimeField(null=True, blank=True)
    is_enter = models.BooleanField(default=False)
    is_theft = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.users.name + ' in ' + self.merchants.name)
    
class PaymentMethod(models.Model):
    TYPE = (
        ('OTOMATIS', 'OTOMATIS'),
        ('MANUAL', 'MANUAL')
    )
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default="085266761420")
    nameholder = models.CharField(max_length=50)
    type = models.CharField(max_length=8, choices=TYPE)

    def __str__(self):
        return self.name

class TopUpHistory(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('SUCCESS', 'SUCCESS'),
        ('CANCELED', 'CANCELED')
    )

    users = models.ForeignKey(to = "User", on_delete=models.CASCADE)
    record = models.CharField(max_length=8, default=genTicket)
    time = models.DateTimeField(default=currentDate.replace(tzinfo=timezone('Asia/Jakarta')))
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    total = models.IntegerField()
    receive = models.IntegerField()
    codeunik = models.IntegerField(default=000)
    status = models.CharField(max_length=8, choices=STATUS)
    ref = models.CharField(max_length=50, default="-")
    datepaid = models.CharField(max_length=50, default="-")
    frompaid = models.CharField(max_length=50, default="-")

    def __str__(self):
        return f"{self.record} | {self.status} - {self.total} | {self.method.name}"