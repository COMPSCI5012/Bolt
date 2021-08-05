# from bolt.views import fqa
from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from bolt.models import Animal, Shelter, UserProfile, Fqa

class ShelterForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter shelter name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    contact_number = forms.CharField(max_length=16, help_text="Enter contact number.")
    address = forms.CharField(max_length=128, help_text="Enter address.")

    class Meta:
        model = Shelter
        fields = ('name','contact_number','address')


#EDIT Form as required
class AnimalForm(forms.ModelForm):

    name = forms.CharField(max_length=32, help_text="Enter animal name")

    KINDS_OF_ANIMALS_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('FISH', 'Fish'),
        ('OTHER', 'Other'),
    ]
    kind = forms.CharField(widget=forms.Select(choices=KINDS_OF_ANIMALS_CHOICES))
    picture = forms.ImageField(help_text="Upload picture", required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=256, help_text="Enter description", required=False)
    date_of_arrival = forms.DateField(widget=forms.DateInput(), required=False)
    adoption_status = forms.CharField(widget=forms.HiddenInput(), required=False)
    adoption_date = forms.CharField(widget=forms.HiddenInput(), required=False)
    

    class Meta:
        model = Animal
        exclude = ('shelter',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'contact_number', 'address', 'picture')

class FqaForm(forms.ModelForm):
    email = forms.CharField(max_length=32)
    content = forms.CharField(max_length=256)

    class Meta:
        model = Fqa
        fields = ('email','content')