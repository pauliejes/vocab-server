from django import forms

class LoginForm(forms.Form):
    userName = forms.CharField(label='User name', max_length=10)
