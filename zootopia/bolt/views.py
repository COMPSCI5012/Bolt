from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from bolt.models import Shelter, Animal
from bolt.forms import AnimalForm, ShelterForm

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


def add_shelter(request):
    form = ShelterForm()
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/bolt/')
        else:
            print(form.errors)
    return render(request, 'bolt/add_shelter.html', {'form':form})

def add_animal(request, shelter_name_slug):
    try:
        shelter = Shelter.objects.get(slug=shelter_name_slug)
    except Shelter.DoesNotExist:
        shelter = None
    
    if shelter is None:
        return redirect('/bolt/')

    form = AnimalForm()
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            if shelter:
                animal = form.save(commit=False)
                animal.shelter = shelter
                animal.save()
                return redirect(reverse('bolt:show_shelter',
                                kwargs={'shelter_name_slug':shelter_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form':form, 'shelter':shelter}
    return render(request, 'bolt/add_animal.html',context=context_dict)