from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Richiesto. Fornisci un indirizzo email valido.')
    email_conf = forms.EmailField(max_length=254, help_text='Richiesto. Conferma l\'indirizzo email.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'email_conf', 'password1', 'password2', )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get('email')
        email_conf = cleaned_data.get('email_conf')

        if email and email_conf and email != email_conf:
            self._errors['email_conf'] = self.error_class(['Le email inserite non coincidono'])
            del self.cleaned_data['email_conf']

        return cleaned_data
