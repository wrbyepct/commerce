from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, AuctionListing


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
            label= 'Username',
            widget= forms.TextInput(attrs={"title": "Enter your username"})
        )     
    
    email = forms.CharField(
            widget= forms.TextInput(attrs={"title": "Enter valid email address."})
        )    
     
    password1 = forms.CharField(
        label='Enter password',
        widget= forms.PasswordInput(attrs={
            "title": """Your password can’t be too similar to your other personal information.
Your password must contain at least 8 characters.
Your password can’t be a commonly used password.
Your password can’t be entirely numeric."""})
    )
    
    password2 = forms.CharField(
        label='Confirm password',
        widget= forms.PasswordInput(attrs={
            "name": "confirmation",
            "title": """Re-enter your password."""})
    )
    
    birthday = forms.DateField(
        label = 'Date of Birth',
        widget= forms.DateInput(attrs={
            'type': 'date',
            'title': 'Pick your birth date from the calendar or type it in YYYY-MM-DD format.'
        }),
        required=False
    )
    
    required_css_class = 'required'
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birthday',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
    
        
class NewListingForm(forms.ModelForm):

    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_bid', 'image']
        labels = {
            'current_bid': 'Starting Bid'
        }
        widgets = {
            'current_bid': forms.NumberInput(attrs={'min': '0.01'})
        }
       
        
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
            

