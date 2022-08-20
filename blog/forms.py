from dataclasses import fields
from logging import PlaceHolder
from pyexpat import model
from tkinter import Widget
from django import forms
from .models import User,Article,Tag
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm)

class Registration(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','PlaceHolder':'Enter the Password'})),
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','PlaceHolder':'Enter the Password'}))

    class Meta:
        model = User
        fields = ['username','password1','password2']

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the User name'}),
        }

class Userlogin(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','PlaceHolder':'Enter the Password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','PlaceHolder':'Enter the Password'}))

    class Meta:
        model = User
        fields = ['username','passsword']

class articleview(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content','img','status']

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Title'}),
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter the Content'}),
            # 'tags':forms.TextInput(attrs={'class':'form-control','Placeholder':'A comma-seperated list of tags'}),

            'img':forms.FileInput(attrs={'class':'form-control'}),
        }


# class Tagsview(forms.ModelForm):
#     class Meta:
#         model = Article_tag
#         fields = ['tags',]

#         widgets = {
#             'tags':forms.TextInput(attrs={'class':'form-control','placeholder':'A Comma-separated list of tags'})
#         }