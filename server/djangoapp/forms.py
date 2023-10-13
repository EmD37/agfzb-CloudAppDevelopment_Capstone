from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control"}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))

class SignupForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    firstname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': "form-control"}))
