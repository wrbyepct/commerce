from django import forms
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

import decimal
from .models import User, AuctionListing, Category, Bid, Comment
from .utils import only_contains_word_or_empty_string

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
        widget= forms.DateInput(
            attrs={
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
        fields = ['title', 'description', 'image']
    
    starting_bid = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'min': 0.01, 'step': 0.01}),
        validators=[MinValueValidator(decimal.Decimal('0.01'))]
    )
    
    new_category = forms.CharField(
        max_length=255, 
        required=False,
        label="Or create a new category"
    )
    
    category = forms.ModelChoiceField(
        # This automatically check for valid choice
        queryset=Category.objects.all(),
        initial=Category.objects.get(id=1),
        label="Choose a category"
    )
    
    def clean_category(self):
        # Check for valid new cate
        new_cate = self.cleaned_data['new_category'].lower().strip()
        if not only_contains_word_or_empty_string(new_cate):
            raise ValidationError('The category must only contain alphabetic characters without space.')
        
        # Check if the name has already existed
        if new_cate != "":
            try:
                category = Category(name=new_cate)
                category.save()
                return category # The instance returns the name of the category
            except IntegrityError:
                raise ValidationError("Category with this name already exists.")
        
        # If new cate is empty, then return selected value   
        return self.cleaned_data['category']
       
        
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['category'].required = False
        
            

class PlaceBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        
        widgets = {
            'price': forms.NumberInput(attrs={
                'id': 'bidInput',
                'step': 0.01,
            })
        }
    
    
    def __init__(self, *args, **kwargs):
        custom_min_value = kwargs.pop('custom_min_value', None)
        super(PlaceBidForm, self).__init__(*args, **kwargs)
        if custom_min_value:
            self.fields['price'].widget.attrs['min'] = custom_min_value
            self.fields['price'].widget.attrs['value'] = custom_min_value
            self.fields['price'].widget.attrs['class'] = 'w-100'
    
    def clean_price(self):
        # Prevent user from tampering with frontend fields
        custom_min_value = self.fields['price'].widget.attrs['min']
        user_input_value = self.cleaned_data['price']
        
        if user_input_value < custom_min_value:
            raise ValidationError('Your bid should be higher than current price')
        
        return user_input_value
   
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'cols': 50,
                'rows': 4,
                'placeholder': "Leave a Commnet...",
                'style': 'resize: none;'
            })
        }