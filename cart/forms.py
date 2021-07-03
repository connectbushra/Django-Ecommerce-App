from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Address
payment_option=(
    ('S','stripe'),
    ('P','paypal'),
    ('V' ,'Visa')
)
class checkout_form(forms.Form):
    country=CountryField(blank_label='(select country)').formfield(
        required=False,widget=CountrySelectWidget( attrs = {
        'class': 'custom-select d-block w-100'
    }))

class SearchForm(forms.Form):
    query=forms.CharField(max_length=100)
    catid=forms.IntegerField()

