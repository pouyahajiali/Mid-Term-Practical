from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Textbook
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    concordia_id = forms.CharField(
        max_length=20,
        required=True,
        help_text="University ID",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Concordia ID'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['concordia_id', 'password1', 'password2']

    def clean_password2(self):
        # Ensure that password1 and password2 match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return password2

    def clean_concordia_id(self):
        concordia_id = self.cleaned_data['concordia_id']
        if User.objects.filter(concordia_id=concordia_id).exists():
            raise ValidationError("A user with this Concordia ID already exists.")
        return concordia_id


class TextbookForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = ['title', 'author', 'edition', 'condition', 'course_code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the textbook title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author(s)'}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2nd Edition'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., COMP346'}),
        }

    def clean_course_code(self):
        course_code = self.cleaned_data['course_code']
        if not course_code.isalnum():
            raise forms.ValidationError("Course code must be alphanumeric.")
        return course_code
