from django import forms
from core.models import User, Vendor


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
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
