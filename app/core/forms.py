""" includes the djnago form and the validators for the forms """
import os
from django import forms
from core.models import User, Vendor, UserProfile
from django.core.exceptions import ValidationError


def image_validator(value):
    """validator shows error if files uploaded other than image."""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ('.png', '.jpg', '.jpeg')

    if not ext.lower() in valid_extensions:
        raise ValidationError(
            f'Unsupported file. Only file with extensions {str(valid_extensions)} are allowed')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')

        if password != conf_password:
            raise forms.ValidationError(
                'Password does not match!'
            )


class RegisterVendorForm(forms.ModelForm):
    vendor_license = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[image_validator])

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[image_validator])
    cover_picture = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[image_validator])
    address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Start Typing...', 'required': 'required'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_picture', 'address',
                  'country', 'state', 'post_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
