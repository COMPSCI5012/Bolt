from django import forms
from bolt.models import Animal, Shelter

class ShelterForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter shelter name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    contact_number = forms.CharField(max_length=16, help_text="Enter contact number.")
    address = forms.CharField(max_length=128, help_text="Enter address.")

    class Meta:
        model = Shelter
        fields = ('name','contact_number','address')

class AnimalForm(forms.ModelForm):

    name = forms.CharField(max_length=32, help_text="Enter animal name")
    kind = forms.CharField(max_length=10, help_text="Enter kind of animal")
    picture = forms.ImageField(help_text="Upload picture", required=False)
    description = forms.CharField(max_length=256, help_text="Enter description", required=False)
    date_of_arrival = forms.DateField(help_text="Enter date of admission")
    adoption_status = forms.CharField(widget=forms.HiddenInput(), required=False)
    adoption_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Animal
        exclude = ('shelter',)