from django import forms
from django.shortcuts import redirect
from django.db.models import Q
# from .models import CustomUser 用下面的方法取得User模型
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Profile


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
    # def is_valid(self):
    #     result = super().is_valid()
    #     # loop on *all* fields if key '__all__' found else only on errors:
    #     for x in (self.fields if '__all__' in self.errors else self.errors):
    #         attrs = self.fields[x].widget.attrs
    #         attrs.update({'class': attrs.get('class', '') + ' is-invalid',
    #                       'value': '{{ field.value }}'})
    #     return result

    class Meta:
        model = get_user_model()

        fields = ('first_name', 'last_name', 'username', 'email',)
        labels = {
            'email': _('Email address'),
            'first_name': _('First name'),
            'last_name': _('Last name')
        }

        error_messages = {
            'username': {
                'unique': _("Username has been used.")
            },
            'email': {
                'unique': _('Email has been used.')
            },
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), required=True)
    password = forms.CharField(label=_('Password'), required=True)

    def clean(self):
        cleaned_data = super().clean()
        user_model = get_user_model()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = user_model.objects.filter(Q(username__iexact=username)).first()
        '''
        用user.check_password(password)來驗證password，不能用model，model中的password是亂碼
        '''
        mismatch = bool(user and not user.check_password(password))
        invalid = bool(not user)
        if mismatch:
            error = ValidationError(message="Username and password don't match !",
                                    code='mismatch')
            self.add_error('password', error)
            self.add_error('username', error)

        if invalid:
            error = ValidationError(message="Invalid username!",
                                    code='invalid')
            self.add_error('username', error)
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'email': _('Email Address'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
