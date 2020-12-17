from django.contrib import admin
from django.utils.safestring import SafeString
from . import models as db
from django.shortcuts import redirect, render
from uuid import uuid4
# Register your models here.

class Feature:
    def mass_add_barcode(self, request, queryset):
        for q in queryset:
            for b in range(0, q.stocks):
                db.ItemBarcode(
                    items = q,
                    barcode = q.name[:5].upper() + uuid4().hex[:7].upper()
                ).save()
        return redirect('/admin/Cashier/itembarcode/')
    
    def show_barcode(self, request, queryset):
        listbarcode = []
        for q in queryset:
            listbarcode.append(q.barcode)
        context = {
            "barcode": listbarcode
        }
        return render(request, 'generatebarcode.html', context)
    
    show_barcode.short_description = "Show Barcode"
    mass_add_barcode.short_description = "Mass Create Barcode"
    
    def mass_unuse_barcode(self, requests, queryset):
        for q in queryset:
            db.ItemBarcode.objects.filter(id = q.id).update(is_used = False)
    mass_unuse_barcode.short_description = "Mass Un Use Barcode"
@admin.register(db.User)
class UserClass(admin.ModelAdmin):
    search_fields = ['email', 'name']
    list_display = ['email', 'name', 'balance']
    list_per_page = 10
    
@admin.register(db.Merchant)
class MerchantClass(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'location', 'balance']
    list_per_page = 10
    
@admin.register(db.Transaction)
class TransactionClass(admin.ModelAdmin):
    search_fields = ['record']
    list_display = ['record', 'users', 'merchants', 'total', 'time', 'is_paid', 'is_success']
    list_per_page = 10
    
@admin.register(db.Item)
class ItemClass(admin.ModelAdmin, Feature):
    search_fields = ['name']
    list_display = ['name', 'unit', 'price', 'merchants', 'stocks']
    actions = ["mass_add_barcode"]
    list_per_page = 10
    
@admin.register(db.TopUpHistory)
class topupProps(admin.ModelAdmin):
    search_fields = ['record']
    list_display = ['record', 'users', 'total', 'method', 'status']
    list_per_page = 10
    
@admin.register(db.MerchantBarcode)
class MerchantBarcodeClass(admin.ModelAdmin):
    search_fields = ['barcode']
    list_display = ['merchants', 'type', 'barcode', 'transactions', 'barcode_image']
    list_per_page = 10
    
    def barcode_image(self, q):
        return SafeString(f"<img src='/qr_show/{q.barcode}/' width='100'/>")
    
@admin.register(db.RemainingCustomer)
class RemainingCustomerClass(admin.ModelAdmin):
    list_display = ['users', 'merchants', 'enterTime', 'exitTime', 'is_theft', 'on_off_theft']
    list_per_page = 10
    
    def on_off_theft(self, q):
        malingkah = "DIA MALING" if not q.is_theft else "DIA BUKAN MALING"
        return SafeString(f'<a href="/on-off-theft/{q.id}" class="changelink">{malingkah}</a>')
    
@admin.register(db.ItemBarcode)
class ItemBarcodeClass(admin.ModelAdmin, Feature):
    search_fields = ['barcode']
    list_display = ['items', 'barcode', 'is_used', 'barcode_image']
    actions = ['mass_unuse_barcode', 'show_barcode']
    list_per_page = 10
    
    def barcode_image(self, q):
        return SafeString(f"<img src='/qr_show/{q.barcode}/' width='100'/>")
    
@admin.register(db.SubTransaction)
class SubTransactionClass(admin.ModelAdmin):
    list_display = ['transactions', 'items', 'quantity']
    list_per_page = 10
    
admin.site.register(db.PaymentMethod)
