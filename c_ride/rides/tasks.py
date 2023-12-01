from config import celery_app


@celery_app.task(name="disable_finished_rides")
def disable_finished_rides():
    """Disable finished rides."""
    from django.utils import timezone

    from c_ride.rides.models import Ride

    now = timezone.now()
    print("now", now)
    # Update rides that have already finished
    rides = Ride.objects.filter(is_active=True, arrival_date__lte=now)
    print("rides", rides)
    rides.update(is_active=False)
    print("rides", rides)
    return f"{rides.count()} rides were disabled."
