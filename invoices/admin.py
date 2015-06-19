from django.contrib import admin

from invoices.models import Invoice, MPESAReceipt


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'customer', 'amount', 'currency', 'method', 'status']
    list_filter = ['customer', 'method', 'status']
    date_hierarchy = 'date'
    search_fields = ['id', 'customer__name', 'customer__id']


class MPESAReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt', 'customer', 'invoice']
    list_filter = ['customer']
    date_hierarchy = 'created_on'
    search_fields = ['receipt', 'customer__name', 'invoice__id']

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(MPESAReceipt, MPESAReceiptAdmin)
