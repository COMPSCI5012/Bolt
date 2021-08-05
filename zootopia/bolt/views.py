from django.shortcuts import render
from django.http import HttpResponse
from bolt.models import Shelter, Animal


# Create your views here.
def index(request):
    shelter_list = Shelter.objects.all()
    context_dict = {}
    context_dict['shelters'] = shelter_list
    return render(request, 'bolt/index.html', context=context_dict)

def about(request):
    return render(request, 'bolt/about.html')

def show_shelter(request, shelter_name_slug):
    context_dict = {}
    try:
        shelter = Shelter.objects.get(slug=shelter_name_slug)
        animals = Animal.objects.filter(shelter=shelter)

        context_dict['shelter'] = shelter
        context_dict['animals'] = animals
    except Shelter.DoesNotExist:
        context_dict['shelter'] = None
        context_dict['animals'] = None
    return render(request, 'bolt/shelter.html', context=context_dict)
