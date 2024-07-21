from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import JSONField  # This requires PostgreSQL


class BookingManager(models.Manager):
    def update_or_create_booking(self, user, booking_instance, customer_name, table_type):
        initial_structure = {
            "table_for_2": 0,
            "table_for_4": 0
        }

        booking, created = self.get_or_create(
            booking_instance=booking_instance,
            defaults={
                'user': user,
                'customer_name': customer_name,
                'tables': initial_structure,
                'slug': slugify(booking_instance)
            }
        )

        if not created:
            if booking.tables[table_type] < 5:
                booking.tables[table_type] += 1
                booking.save()
                UserBooking.objects.create(booking=booking, user=user, booking_instance=booking_instance, table_type=table_type)
                return booking, table_type

        if created:
            if booking.tables[table_type] < 5:
                booking.tables[table_type] += 1
                booking.save()
                UserBooking.objects.create(booking=booking, user=user, booking_instance=booking_instance, table_type=table_type)
                return booking, table_type

        return None, None

    def cancel_booking(self, user_booking_id):
        try:
            user_booking = UserBooking.objects.get(id=user_booking_id)
            booking = user_booking.booking
            table_type = user_booking.table_type

            if booking.tables[table_type] > 0:
                booking.tables[table_type] -= 1
                booking.save()
                user_booking.delete()
                return True
            return False
        except UserBooking.DoesNotExist:
            return False


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_instance = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=100)
    tables = JSONField(default=dict)  # JSON field to store table availability
    slug = models.SlugField(max_length=200, blank=True)

    objects = BookingManager()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.booking_instance)
        super().save(*args, **kwargs)

class UserBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='user_bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_instance = models.CharField(max_length=100)
    table_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.booking_instance} - {self.table_type}"

