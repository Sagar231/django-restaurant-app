from django import forms
import datetime

class BookingForm(forms.Form):
    DATE_CHOICES = [
        ('noon', '12 PM to 3 PM'),
        ('night', '8 PM to 12 AM')
    ]

    TABLE_CHOICES = [
        ('table for 2', 'Table for 2'),
        ('table for 4', 'Table for 4')
    ]

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        })
    )
    time = forms.ChoiceField(choices=DATE_CHOICES)
    table_type = forms.ChoiceField(choices=TABLE_CHOICES)
    customer_name = forms.CharField(max_length=100)

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today() + datetime.timedelta(days=1):
            raise forms.ValidationError("The date cannot be today or in the past!")
        return date

class CancelBookingForm(forms.Form):
    table_type_choices = [
        ('table for 2', 'Table for 2'),
        ('table for 4', 'Table for 4')
    ]

    booking_instance = forms.CharField(max_length=100)
    table_type = forms.ChoiceField(choices=table_type_choices)
    table_number = forms.CharField(max_length=10)
