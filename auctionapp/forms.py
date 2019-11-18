from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Your email')

class NewItemForm(forms.Form):
    title = forms.CharField(label='Item Title', max_length=200, required=True)
    description = forms.CharField(label='Description', max_length=500, required=False)
    image = forms.ImageField(label='Add a Picture', required=False)
    start_price = forms.DecimalField(label='Starting Price', initial='0.00', max_digits=10, decimal_places=2, required=True)
    end_time = forms.DateTimeField(label='End Time (dd/mm/yyyy hh:mm)', input_formats=['%d/%m/%Y %H:%M'], initial='31/12/2019 12:00', required=True)