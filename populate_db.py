"""This is script is meant to be run only locally, not in production

Copy and paste this script in the Django shell to populate the database with
dummy data.
"""

import csv
import random
from datetime import timedelta

from django.utils import timezone

from c_ride.circles.models import Circle, Membership
from c_ride.rides.models import Ride
from c_ride.users.models import Profile, User


def load_circles(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        for row in rows:
            c = Circle.objects.create(
                name=row[0],
                slug_name=row[1],
                is_public=row[2] == "1",
                verified=row[3] == "1",
                is_limited=row[4] != "0",
                members_limit=0 if row[4] == "0" else int(row[4]),
            )
            print(c)


load_circles("circles.csv")

n_users = 60
users = []
for _ in range(n_users):
    user = User.objects.create(
        email=f"dummyuser{_}@gmail.com",
        name=f"uniquerusername00{_}",
        password="vanderpapi",
    )
    Profile.objects.create(user=user)
    users.append(user)
    print("New user create", user.email)

circles = Circle.objects.all()

for circle in circles:
    for user in users:
        m = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            remaining_invitations=10,
        )
        print("New member added", m)


for circle in circles:
    for offerer in random.choices(users, k=random.randint(1, 10)):
        available_seats = random.randint(1, 8)
        now = timezone.now()
        departure = now + timedelta(
            hours=(random.choice([1, -1])) * random.randint(1, 10)
        )
        ride = Ride.objects.create(
            offered_by=offerer,
            offered_in=circle,
            available_seats=available_seats,
            departure_location="Departure location",
            arrival_location="Arrival location",
            departure_date=departure,
            arrival_date=departure + timedelta(hours=1),
        )
        passengers = random.choices(users, k=random.randint(1, available_seats))
        passengers = [u for u in passengers if u != offerer]
        ride.passengers.add(*passengers)
        ride.save()
        print("New ride created", ride)
