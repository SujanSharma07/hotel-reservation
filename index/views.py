# Create your views here.
from django.shortcuts import render
from django.db.models import Count


from hotels.models import *
from index.models import *


def index(request):
    hotels = Hotels.objects.all()
    popular_hotels=Hotels.objects.annotate(num_bookings=Count('booking')).order_by('-num_bookings')[:3]


    return render(request, "index.html", {"hotels": hotels,"pop_hotels":popular_hotels})
