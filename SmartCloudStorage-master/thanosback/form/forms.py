from django import forms

class Formsignup(forms.Form):
    email=forms.CharField(max_length=30,label='email')
    password=forms.CharField(max_length=29,label='password')

