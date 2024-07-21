from django.contrib import admin
from django.utils.text import slugify
from .models import Booking, UserBooking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_instance', 'customer_name', 'tables', 'slug')
    search_fields = ('booking_instance', 'customer_name')
    readonly_fields = ('slug',)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.booking_instance)
        obj.save()

class UserBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_instance', 'table_type', 'booking')
    search_fields = ('user__username', 'booking_instance', 'table_type')

admin.site.register(Booking, BookingAdmin)
admin.site.register(UserBooking, UserBookingAdmin)
