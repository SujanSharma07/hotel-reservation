# Create your views here.
from django.shortcuts import render

from hotels.models import *
from index.models import *


def index(request):
    hotels = Hotels.objects.all()

    return render(request, "index.html", {"hotels": hotels})
