from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_table, name='book_table'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
