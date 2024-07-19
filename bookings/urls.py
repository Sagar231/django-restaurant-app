from django.urls import path
from . import views

urlpatterns = [
    path('book_table/', views.book_table, name='book_table'),
    path('cancel_booking/', views.cancel_booking, name='cancel_booking'),
]
