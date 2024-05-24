from django.urls import path

from . import views

urlpatterns = [
    path("bookroom/<hotelid>/<roomtype>", views.bookroom, name="bookroom"),
    path(
        "new/<hotelid>/<roomid>/<totalcost>/", views.storeBooking, name="storeBooking"
    ),
    path("mybookings", views.mybookings, name="mybookings"),
    path(
        r"^mybookings/cancel/(?P<bid>[0-9]+)$",
        views.cancelbooking,
        name="cancelbooking",
    ),
]
