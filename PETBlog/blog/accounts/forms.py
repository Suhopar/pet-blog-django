from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """

    User registration form with advanced fields.

    """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    ROLE_CHOICES = [
        ('user', 'User (Default)'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='user', widget=forms.HiddenInput())
    usual_ban = forms.BooleanField(required=False, widget=forms.HiddenInput())
    absolute_ban = forms.BooleanField(required=False, widget=forms.HiddenInput())
    user_about = forms.CharField(max_length=500,widget=forms.Textarea,  required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_about',
                  'profile_image', 'password1', 'password2', 'role']

    def clean_password2(self):
        return self.cleaned_data.get("password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.usual_ban = self.cleaned_data['status_ban']
        user.absolute_ban = self.cleaned_data['absolute_ban']
        user.user_about = self.cleaned_data['user_about']
        user.profile_image = self.cleaned_data['profile_image']



        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    user_about = forms.CharField(max_length=500,widget=forms.Textarea,  required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'user_about', 'profile_image')
