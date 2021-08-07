from django.db import models
from datetime import date
from django.db.models.base import Model
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

'''
Check installed apps for phonenumber_field, for contact number
#from phonenumber_field.modelfields import PhoneNumberField

Check if database can be changed to pg which supports Composite field for Address
#from django_pg import models
'''

# class Address(CompositeField):
#     line1 = models.CharField(max_length=128)
#     line2 = models.CharField(max_length=128, blank=True, null=True)
#     postcode = models.CharField()
#     city = models.CharField(max_length=32)

class Shelter(models.Model):
    name = models.CharField(max_length=128, unique=True)
    #contact_number = PhoneNumberField(null=False, blank=False, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    #address = Address()
    address = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Shelter, self).save(*args, **kwargs)

    #Modify to show only those animals that are currently in shelter
    @property
    def number_of_animals(self):
        return self.animal_set.count()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    #Make a check, if is_caretaker is True, user must have an assigned shelter
    is_caretaker = models.BooleanField(default=False)
    shelter = models.OneToOneField(Shelter, models.SET_NULL, null=True, blank=True, related_name='caretaker')

    def __str__(self):
        return self.user.username


class Animal(models.Model):    
    #Animal can exist in database without a shelter allocated or a adopter
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=32, default="John Doe")
    KINDS_OF_ANIMALS_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('FISH', 'Fish'),
        ('OTHER', 'Other'),
    ]
    kind = models.CharField(max_length=10, choices=KINDS_OF_ANIMALS_CHOICES, default='DOG')
    description = models.TextField(max_length=256, blank=True)
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    date_of_arrival = models.DateField(null=True, blank=True, default=date.today)
    
    def __str__(self):
        return self.name
    
    @property
    def adoption_status(self):
        requests = Adopt.objects.filter(animal=self)
        if requests:
            for request in requests:
                if request.status == 'ACCEPTED':
                    return 'ADOPTED'
            return 'REQUESTED'
        return 'NOT_ADOPTED'

    @property
    def adoption_date(self):
        requests = Adopt.objects.filter(animal=self)
        if requests:
            for request in requests:
                if request.status == 'ACCEPTED':
                    return request.adoption_date
        return None



class Fqa(models.Model):
    email = models.CharField(max_length=32)
    content = models.CharField(max_length=256)


class Adopt(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='adopter')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    caretaker = models.ForeignKey(UserProfile, models.SET_NULL, blank=True, null=True, related_name='caretaker')
    request_date = models.DateField(blank=True, default=date.today)
    adoption_date = models.DateField(blank=True, default=date.today)
    ADOPTION_REQUETS_CHOICES = [
        ('ACCEPTED','Accepted'),
        ('PENDING','Pending'),
        ('REJECTED','Rejected'),
    ]
    status = models.CharField(max_length=10, choices=ADOPTION_REQUETS_CHOICES, default='PENDING', blank=True)

    @property
    def animal_shelter(self):
        return self.animal.shelter

    def __str__(self):
        return f"{self.user} -> {self.animal.name}"