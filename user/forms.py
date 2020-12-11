from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        required=True,
        help_text="Must be at least 8 characters long and can't be entirely numeric",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Verify Password'),
        required=True,
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError(message=_('Password must be the same as above.'),
                                  code='notmatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def is_valid(self):
        result = super().is_valid()
        # loop on *all* fields if key '__all__' found else only on errors:
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result

    class Meta:
        model = CustomUser

        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'email': _('Email address'),
        }

        error_messages = {
            'username': {
                'unique': _("Username has been used.")
            },
            'email': {
                'unique': _('Email has been used.')
            },
        }

        # 'oninvalid': "setCustomValidity('This is required')",
        # 'oninput': "setCustomValidity('')"