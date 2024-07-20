from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm,CancelBookingForm

@login_required
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            table_type = form.cleaned_data['table_type']
            customer_name = form.cleaned_data['customer_name']

            booking_instance = f"{date.strftime('%d-%m-%Y')}{time}"
            user = request.user

            booking, table = Booking.objects.update_or_create_booking(user, booking_instance, customer_name, table_type)

            if table:
                return JsonResponse({'status': 'success', 'message': f'Table {table} booked successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No available tables for the selected time and type.'})
    else:
        form = BookingForm()

    return render(request, 'book_table.html', {'form': form})


@login_required
def cancel_booking(request):
    if request.method == 'POST':
        form = CancelBookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.cleaned_data['booking_instance']
            table_type = form.cleaned_data['table_type']
            table_number = form.cleaned_data['table_number']

            success = Booking.objects.cancel_booking(booking_instance, table_type, table_number)

            if success:
                return JsonResponse({'status': 'success', 'message': f'Booking for {table_number} cancelled successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Could not cancel the booking. Please check the details and try again.'})
    else:
        form = CancelBookingForm()

    return render(request, 'cancel_booking.html', {'form': form})
