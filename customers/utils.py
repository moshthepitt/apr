def customer_has_subscription(customer):
    """
    returns true is the customer has a relation to a CustomerSubscription object
    """
    from subscriptions.models import CustomerSubscription

    try:
        return customer.customersubscription is not None
    except CustomerSubscription.DoesNotExist:
        return None
