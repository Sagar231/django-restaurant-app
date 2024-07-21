from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, UserBooking
from .forms import BookingForm
from django.contrib import messages

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
                messages.success(request, f'Table {table} booked successfully!')
                form = BookingForm()  # Clear the form
            else:
                messages.error(request, 'No available tables for the selected type at the perticular time.')
                form = BookingForm()  # Clear the form
    else:
        form = BookingForm()

    return render(request, 'bookings/book_table.html', {'form': form})


@login_required
def my_bookings(request):
    user_bookings = UserBooking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'user_bookings': user_bookings})


@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        success = Booking.objects.cancel_booking(booking_id)
        if success:
            messages.success(request, 'Booking cancelled successfully!')
        else:
            messages.error(request, 'Could not cancel the booking. Please try again.')
        
        # Redirect back to my_bookings with a message
        return redirect('my_bookings') 

    return redirect('my_bookings')
