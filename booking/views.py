import datetime

import paypalrestsdk
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from hotels.models import *
from hotels.models import Booking
from index.models import *

from .paypal_config import *


# Create your views here.
def bookroom(request, hotelid, roomtype):
    FirstDate = request.session["arrival"]
    SecDate = request.session["departure"]
    if FirstDate and SecDate:
        Checkin = datetime.datetime.strptime(FirstDate, "%Y-%m-%d").date()
        Checkout = datetime.datetime.strptime(SecDate, "%Y-%m-%d").date()
    else:
        Checkin = datetime.date.today()
        Checkout = Checkin + datetime.timedelta(days=1)
        request.session["arrival"] = str(Checkin)
        request.session["departure"] = str(Checkout)

    timedeltaSum = Checkout - Checkin

    StayDuration = int(timedeltaSum.days)

    hotel = Hotels.objects.get(hotel_id__exact=hotelid)
    rooms = Room.objects.filter(hotel_id__exact=hotelid).filter(
        RoomType__exact=roomtype
    )
    for room in rooms:
        price = room.Price
    TotalCost = StayDuration * int(price)

    context = {
        "checkin": Checkin,
        "checkout": Checkout,
        "stayduration": StayDuration,
        "hotel": hotel,
        "rooms": rooms,
        "price": price,
        "totalcost": TotalCost,
    }
    return render(request, "booking.html", context)


def storeBooking(request, hotelid, roomid, totalcost):
    if request.method == "POST" and request.user.is_authenticated:

        Firstname = request.POST.get("firstname")
        Lastname = request.POST.get("lastname")
        checkin = request.session["arrival"]
        checkout = request.session["departure"]
        user = request.user
        hotel = Hotels.objects.get(hotel_id__exact=hotelid)
        room = Room.objects.get(id=roomid)
        cost = totalcost
        newReservation = Booking.objects.create(
            hotel_id=hotel,
            roomtype=room.RoomType,
            user=user,
            guestFirstName=Firstname,
            guestLastName=Lastname,
            CheckIn=checkin,
            CheckOut=checkout,
            totalPrice=cost,
        )
        # newReservation.hotel_id = hotel
        # newReservation.roomtype = room.RoomType
        # newReservation.user = user
        # newReservation.guestFirstName = Firstname
        # newReservation.guestLastName = Lastname
        # newReservation.CheckIn = checkin
        # newReservation.CheckOut = checkout
        # newReservation.totalPrice = cost
        newReservation.save()
        # Deletes the session variables.
        # del request.session['arrival']
        # del request.session['departure']
        bid = newReservation.id
        bookings = Booking.objects.filter(id=bid)

        return render(request, "mybookings.html", {"bookings": bookings})
    else:
        return redirect("/accounts/login")


def mybookings(request):
    bookings = Booking.objects.filter(user=request.user)
    context = {"bookings": bookings}
    return render(request, "mybookings.html", context)


def cancelbooking(request, bid):
    booking = Booking.objects.filter(id=bid).first()
    if booking:
        if booking.payment_status == "Success":
            messages.info(
                request,
                "Your booking has been canceled. Our staff will contact you for refund and policies.",
            )
        booking.delete()
    else:
        messages.error(request, "Booking not found.")
    return redirect("/booking/mybookings")


def paypal_payment(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")

        # Retrieve booking details using the booking_id
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = Booking.INITIATED
            booking.save()
        except Booking.DoesNotExist:
            return render(request, "payment_error.html", {"error": "Booking not found"})

        # Create PayPal payment
        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(
                        reverse("execute_payment")
                    ),
                    "cancel_url": request.build_absolute_uri(reverse("payment_cancel")),
                },
                "transactions": [
                    {
                        "item_list": {
                            "items": [
                                {
                                    "name": "Booking for {}".format(booking.roomtype),
                                    "sku": "item",
                                    "price": str(booking.totalPrice),
                                    "currency": "USD",
                                    "quantity": 1,
                                }
                            ]
                        },
                        "amount": {"total": str(booking.totalPrice), "currency": "USD"},
                        "description": "Payment for booking ID {}".format(booking_id),
                    }
                ],
            }
        )

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            return render(request, "payment_error.html", {"error": payment.error})
    return render(request, "mybookings.html")


def execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Extract booking ID from payment description
        booking_id = payment.transactions[0].description.split()[-1]

        # Update the booking payment status to SUCCESS
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = Booking.SUCCESS
            booking.save()
        except Booking.DoesNotExist:
            return render(request, "payment_error.html", {"error": "Booking not found"})

        return render(request, "payment_success.html")
    else:
        return render(request, "payment_error.html", {"error": payment.error})


def payment_cancel(request):
    return render(request, "payment_cancel.html")
