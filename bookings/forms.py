from django import forms
import datetime

class BookingForm(forms.Form):
    DATE_CHOICES = [
        ('noon', '12 PM to 3 PM'),
        ('night', '8 PM to 12 AM')
    ]

    TABLE_CHOICES = [
        ('table_for_2', 'Table for 2'),
        ('table_for_4', 'Table for 4')
    ]

    today = datetime.date.today()
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            'max': (today + datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    time = forms.ChoiceField(
        choices=DATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    table_type = forms.ChoiceField(
        choices=TABLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today() + datetime.timedelta(days=1) or date > datetime.date.today() + datetime.timedelta(days=7):
            raise forms.ValidationError("The date must be within the next week!")
        return date
