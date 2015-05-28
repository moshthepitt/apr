from django.contrib import admin

from subscriptions.models import Subscription, CustomerSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_appointments', 'highlighted']


class CustomerSubscriptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CustomerSubscription, CustomerSubscriptionAdmin)
