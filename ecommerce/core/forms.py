from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import User

from .models import Item, ConversationMessage

INPUT_STYLES = 'width: 100%; height: 30px; margin: 10px 0; padding: 0 10px; border: 1px solid #ccc;'
CONVO_STYLES = 'width: 100%; height: 100px; margin: 10px 0; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px;'


# class LoginForm(AuthenticationForm):
#     name = forms.CharField(widget=forms.TextInput(attrs={
#         'style': INPUT_STYLES,
#         'placeholder': 'Username'
#     }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'style': INPUT_STYLES,
#         'placeholder': 'Password'
#     }))

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'style': INPUT_STYLES,
        'placeholder': 'Username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'style': INPUT_STYLES,
        'placeholder': 'Email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'style': INPUT_STYLES,
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'style': INPUT_STYLES,
        'placeholder': 'Repeat password'
    }))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'name', 'username', 'email', 'bio', 'instagram', 'facebook', 'twitter',)

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image1', 'image2', 'image3', 'image4',)

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image1','image2', 'image3', 'image4','is_sold',)
        
class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'style': CONVO_STYLES
            })
        }