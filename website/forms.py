from django import forms
from .models import Account

# model forms


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name','email', 'avatar',)
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }

