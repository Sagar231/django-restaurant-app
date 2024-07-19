from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField  # This requires PostgreSQL

class BookingManager(models.Manager):
    def update_or_create_booking(self, user, booking_instance, customer_name, table_type):
        tables_structure = {
            "table for 2": {
                "table 1": True,
                "table 2": True,
                "table 3": True,
                "table 4": True,
                "table 5": True
            },
            "table for 4": {
                "table 6": True,
                "table 7": True,
                "table 8": True,
                "table 9": True,
                "table 10": True
            }
        }
        
        booking, created = self.get_or_create(
            booking_instance=booking_instance,
            defaults={
                'user': user,
                'customer_name': customer_name,
                'tables': tables_structure,
                'slug': slugify(booking_instance)
            }
        )

        if not created:
            available_tables = booking.tables.get(table_type, {})
            for table, available in available_tables.items():
                if available:
                    available_tables[table] = False
                    booking.tables[table_type] = available_tables
                    booking.save()
                    return booking, table

        if created:
            available_tables = booking.tables.get(table_type, {})
            for table, available in available_tables.items():
                if available:
                    available_tables[table] = False
                    booking.tables[table_type] = available_tables
                    booking.save()
                    return booking, table

        return None, None

    def cancel_booking(self, booking_instance, table_type, table_number):
        try:
            booking = self.get(booking_instance=booking_instance)
            if booking.tables[table_type][table_number] == False:
                booking.tables[table_type][table_number] = True
                booking.save()
                return True
            return False
        except Booking.DoesNotExist:
            return False

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_instance = models.CharField(max_length=100, unique=True)  # Make this unique to avoid duplicates
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

