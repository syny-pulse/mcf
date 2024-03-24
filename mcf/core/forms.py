from core.models import Client_Account, Client_Form_Info
from core import models  # Import model form factory
from django import forms
from .models import Client_Account  # Assuming Client_Account is in your app's models.py


class SearchForm(forms.Form):
    account_number = forms.CharField(label='Account Number')


"""class ClientInfoForm(forms.Form):
    def ClientInfoForm(client_account):
        #    Creates a dynamic form based on the provided client_account instance.

    Args:
        client_account (django.db.models.Model): The client account object.

    Returns:
        django.forms.Form: A dynamically generated form based on the client account's fields.
        #

    fields = {}
    for field in client_account._meta.get_fields():
        if not getattr(client_account, field.name):
            # Only include fields with None values
            field_instance = field
            fields[field.name] = forms.CharField(label=field.verbose_name, required=False)  # Set required=False for optional fields

        return type('ClientInfoForm', (forms.Form,), {'fields': fields})"""



from django import forms

class Client_Info_Form(forms.ModelForm):
    class Meta:
        model = Client_Form_Info
        exclude = '__all__'

    def __init__(self, *args, **kwargs):
        super(Client_Info_Form, self).__init__(*args, **kwargs)
        # Access the passed acctnum from kwargs
        self.initial['ACCTNUM'] = kwargs.get(Client_Account.ACCTNUM)
        # Make the ACCTNUM field read-only
        self.fields['ACCTNUM'].widget.attrs['readonly'] = True






    
