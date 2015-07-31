from django.contrib import admin

from subscriptions.models import Subscription, CustomerSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_appointments', 'default', 'highlighted', 'hidden']


class CustomerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'subscription', 'status']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CustomerSubscription, CustomerSubscriptionAdmin)
