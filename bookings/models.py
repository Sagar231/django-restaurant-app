from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'table_{self.table_number}'


class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    slug = models.SlugField(max_length=200,blank=True)

    def __str__(self):
        return self.slug

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.table)
        super().save(*args,**kwargs)