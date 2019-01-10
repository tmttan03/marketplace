from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.core.validators import validate_email


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput()
    last_name = forms.TextInput()


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
            raise forms.ValidationError('This email address is already in use.')
        except User.DoesNotExist:
            return email
        

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	first_name = forms.TextInput()
	last_name = forms.TextInput()

	class Meta:
		model = User
		fields = ['first_name','last_name','username' , 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']


class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        
           