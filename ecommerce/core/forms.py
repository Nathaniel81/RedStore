"""
Django Forms for User Authentication and Data Input

This module contains Django forms used for user authentication, registration, and user profile
data input. Additionally, it includes forms for creating, editing, and messaging in the context
of items and conversations in the application.

Classes:
    - SignUpForm: User registration form.
    - UserForm: User profile update form.
    - NewItemForm: Form for creating a new item.
    - EditItemForm: Form for editing an existing item.
    - ConversationMessageForm: Form for sending a message in a conversation.
"""


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import User

from .models import Item, ConversationMessage

# CSS styles for input fields
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
    """
    User registration form.
    """
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
    """
    User profile update form.
    """
    class Meta:
        model = User
        fields = ('avatar', 'name', 'username', 'email', 'bio', 'instagram', 'facebook', 'whatsup', 'twitter',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'form-control bio-input'})
        # Remove help text for the username field
        self.fields['username'].help_text = None

class NewItemForm(forms.ModelForm):
    """
    Form for creating a new item.
    """
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image1', 'image2', 'image3', 'image4',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'description-width'

class EditItemForm(forms.ModelForm):
    """
    Form for editing an existing item.
    """
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'is_sold',)

    def __init__(self, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

        # Suppress the clear label for image fields
        for field_name in ('image1', 'image2', 'image3', 'image4'):
            self.fields[field_name].widget.clear_checkbox_label = ''
        
class ConversationMessageForm(forms.ModelForm):
    """
    Form for sending a message in a conversation.
    """
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'style': CONVO_STYLES
            })
        }
