from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator

import decimal
from .models import User, AuctionListing, Category


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
    starting_bid = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(decimal.Decimal('0.01'))]
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=Category.objects.get(id=1),
        label="Choose a category"
    )
    
    new_category = forms.CharField(
        max_length=255, 
        required=False,
        label="Or create a new category"
    )
    
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image']
        widgets = {
            'current_bid': forms.NumberInput(attrs={'min': '0.01', 'step': 0.01})
        }
       
        
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['category'].required = False
        
            

class PlaceBidForm(forms.Form):
    bid_input = forms.DecimalField(min_value=0.01, decimal_places=2)