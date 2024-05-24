from django.urls import path

from . import views

urlpatterns = [
    path("<hotel_id>/", views.hotels, name="hotels"),
]
