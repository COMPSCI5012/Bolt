from django.forms.widgets import DateInput
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from bolt.models import Shelter, Animal, UserProfile, Adopt
from django.contrib.auth.models import User
from bolt.forms import AnimalForm, ShelterForm, UserProfileForm, UserForm, FqaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.
def index(request):
    shelter_list = Shelter.objects.all()
    context_dict = {}
    context_dict['shelters'] = shelter_list

    # visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']

    response = render(request, 'bolt/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {}
    # visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    return render(request, 'bolt/about.html', context=context_dict)

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
    
    try:
        caretaker = shelter.caretaker
        context_dict['caretaker'] = caretaker
    except UserProfile.DoesNotExist:
        context_dict['caretaker'] = None

    return render(request, 'bolt/shelter.html', context=context_dict)


@login_required
def add_shelter(request):
    form = ShelterForm()
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('bolt:adoptions'))
        else:
            print(form.errors)
    return render(request, 'bolt/add_shelter.html', {'form':form})

@login_required
def add_animal(request):
    form = AnimalForm()
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.save()
            return redirect(reverse('bolt:adoptions'))
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request, 'bolt/add_animal.html',context=context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'bolt/register.html', context = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


def fqa(request):
    form = FqaForm()
    if request.method == 'POST':
        form = FqaForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/bolt/')         
        else:
            print(form.errors)
    return render(request, 'bolt/fqa.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('bolt:index'))
            else:
                return HttpResponse('Your Bolt account is disabled.')
        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'bolt/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bolt:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits



@login_required
def adoption_request_reject(request, request_pk):
    try:
        adopt_request = Adopt.objects.get(pk=request_pk)
    except Adopt.DoesNotExist:
        return redirect(reverse('bolt:myaccount'))
    adopt_request.caretaker = request.user.userprofile
    adopt_request.status = 'REJECTED'
    adopt_request.save()
    return redirect(reverse('bolt:myaccount'))


@login_required
def adoption_request_accept(request, request_pk):
    try:
        adopt_request = Adopt.objects.get(pk=request_pk)
    except Adopt.DoesNotExist:
        return redirect(reverse('bolt:myaccount'))

    #Accept current request
    adopt_request.caretaker = request.user.userprofile
    adopt_request.status = 'ACCEPTED'
    adopt_request.animal.user = adopt_request.user
    adopt_request.animal.save()
    adopt_request.adoption_date = datetime.today()
    adopt_request.save()

    #Reject any other pending requests
    pending_requests = Adopt.objects.filter(animal=adopt_request.animal).exclude(pk=request_pk)
    for r in pending_requests:
        r.caretaker = request.user.userprofile
        r.status = 'REJECTED'
        r.save()
    return redirect(reverse('bolt:myaccount'))

#Groups list in 3s, easy to display row
def get_list(animals):
    animals_list = []
    temp_list = []
    i = 0
    for animal in animals:
        temp_list.append(animal)
        i += 1
        if i % 3 == 0:
            i = 0
            animals_list.append(temp_list)
            temp_list = []
    if temp_list != []:
        animals_list.append(temp_list)
    return animals_list

@login_required
def adoptions(request, animal_kind=''):
    context_dict = {}
   
    #Get filtered animals to be displayed
    if animal_kind == '':
        animals = [a for a in Animal.objects.all() if a.adoption_status != 'ADOPTED']
    elif animal_kind == 'Others':
        animals = [a for a in Animal.objects.exclude(kind='DOG').exclude(kind='CAT') if a.adoption_status != 'ADOPTED']
    else:
        animals = [a for a in Animal.objects.filter(kind=animal_kind.upper()) if a.adoption_status != 'ADOPTED']
   
    #Get grouped list of animals
    requested_adoptions = []
    if not animals:
        context_dict['animals_list'] = None
        context_dict['pending_requests'] = None
        return render(request, 'bolt/adoptions.html', context=context_dict)
    
    not_adopted_animal_list = []
    for animal in animals:
        try:
            pending_request = Adopt.objects.get(animal=animal, user=request.user.userprofile)
            if pending_request.status == "PENDING":
                requested_adoptions.append(pending_request)
            else:
                not_adopted_animal_list.append(animal)
        except Adopt.DoesNotExist:
            not_adopted_animal_list.append(animal)

    context_dict['animals_list'] = get_list(not_adopted_animal_list)
    context_dict['pending_requests'] = get_list(requested_adoptions)

    return render(request, 'bolt/adoptions.html', context=context_dict)


@login_required
def make_request(request, animal_pk=0):
    try:
        animal = Animal.objects.get(pk=animal_pk)
        req = Adopt.objects.get_or_create(animal=animal, user=request.user.userprofile)[0]
        req.request_date = datetime.today()
        req.status = "PENDING"
        req.save()
    except Exception as e:
        print(e)
    return redirect(reverse('bolt:adoptions'))




def get_list_of_requests(shelter):
    pending_requests = []
    requests = Adopt.objects.filter(status="PENDING")
    if requests.count() == 0:
        return None
    for request in requests:
        if request.animal_shelter == shelter:
            pending_requests.append(request)
    return tuple(pending_requests)

@login_required
def myaccount(request):
    visitor_cookie_handler(request)
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    context_dict = {'user':user, 'userprofile':userprofile,}
        
    #Get all adopter animal
    if userprofile.animal_set.count() != 0:
        print(userprofile.animal_set.all())
        context_dict['animals'] = userprofile.animal_set.all()
    else:
        context_dict['animals'] = None
    
    #Get all pending requests
    if userprofile.is_caretaker:
        context_dict['shelter'] = userprofile.shelter
        context_dict['requests'] = get_list_of_requests(userprofile.shelter)
    else:
        context_dict['shelter'] = None
        context_dict['requests'] = None
    context_dict['is_caretaker'] = userprofile.is_caretaker

    return render(request, "bolt/myaccount.html", context=context_dict)