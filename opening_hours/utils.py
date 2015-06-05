import datetime

from opening_hours.models import OpeningHour


def new_default_opening_hours(customer):
    """
    creates default opening hours for customer
    """
    times = [(datetime.time(hour=6, minute=0), datetime.time(hour=19, minute=0))]
    bulk_create_opening_hours(times, customer)


def new_default_venue_opening_hours(venue):
    """
    creates default opening hours for venue
    """
    times = [(datetime.time(hour=6, minute=0), datetime.time(hour=19, minute=0))]
    bulk_create_venue_opening_hours(times, venue)


def bulk_create_opening_hours(times, customer):
    """
    convenience function to bulk create opening hours
    Inputs:
        times => a list of tuples, each tuple being (from_hour, to_hour)
                from_hour and to_hour are datetime.time objects
        customer => Customer object
        example code:
            import datetime
            from opening_hours.utils import bulk_create_opening_hours
            a = (datetime.time(hour=10, minute=0), datetime.time(hour=11, minute=0))
            b = (datetime.time(hour=13, minute=0), datetime.time(hour=14, minute=0))
            times = [a, b]
            bulk_create_opening_hours(times, customer)
    """
    venues = customer.venue_set.all()
    for venue in venues:
        for w in OpeningHour.WEEKDAYS:
            weekday = w[0]
            for t in times:
                opening_hour = OpeningHour(
                    venue=venue,
                    customer=customer,
                    weekday=weekday,
                    from_hour=t[0],
                    to_hour=t[1],
                )
                opening_hour.save()


def bulk_create_venue_opening_hours(times, venue):
    """
    convenience function to bulk create opening hours for venue
    Inputs:
        times => a list of tuples, each tuple being (from_hour, to_hour)
                from_hour and to_hour are datetime.time objects
        venue => Venue object
        example code:
            import datetime
            from opening_hours.utils import bulk_create_venue_opening_hours
            a = (datetime.time(hour=10, minute=0), datetime.time(hour=11, minute=0))
            b = (datetime.time(hour=13, minute=0), datetime.time(hour=14, minute=0))
            times = [a, b]
            bulk_create_venue_opening_hours(times, venue)
    """
    for w in OpeningHour.WEEKDAYS:
        weekday = w[0]
        for t in times:
            opening_hour = OpeningHour(
                venue=venue,
                customer=venue.customer,
                weekday=weekday,
                from_hour=t[0],
                to_hour=t[1],
            )
            opening_hour.save()


def get_seconds_since_day_start(exact_time):
    """
    returns the seconds passed since the start of the day 00:00:00
    we assume each day has exactly 86400 seconds i.e. 24 * 60 * 60 seconds
    """
    return (exact_time.hour * 60 * 60) + (exact_time.minute * 60) + exact_time.second


def reverse_get_seconds_since_day_start(time_in_seconds):
    """
    returns time of day from seconds since start of day
    """
    minutes, seconds = divmod(time_in_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return datetime.time(hour=hours, minute=minutes, second=seconds)
