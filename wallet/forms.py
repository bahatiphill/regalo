from django import forms
from wallet.models import  Abatuye, SentPayments


class AbatuyeForm(forms.ModelForm):

    class Meta:
        model = Abatuye
        fields = ['name', 'phone_number', 'amount', 'location', 'reason']
        #exclude = ['timestamp', 'to_church','successful', 'transaction_id']


        def clean(self):
            cleaned_data = super(AbatuyeForm, self).clean()
            phone = cleaned_data.get('phone_number')
            if not phone.startswith('078') or len(data) != 10:
                raise forms.ValidationError('Phone number not correct (Phone number: 078XXXXXXX) and Must be MTN carrier')
                
            return phone



class KubikuzaForm(forms.ModelForm):

    class Meta:
        model = SentPayments
        fields = ['phone_number', 'amount']


        def clean(self):
            cleaned_data = super(KubikuzaForm, self).clean()
            phone = cleaned_data.get('phone_number')
            amount = cleaned_data.get('amount')

            if not phone.startswith('078') or len(data) != 10:
                raise forms.ValidationError('Phone number not correct (Phone number: 078XXXXXXX) and Must be MTN carrier')

            return phone
