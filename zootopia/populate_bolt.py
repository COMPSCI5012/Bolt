import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zootopia.settings')

import django
django.setup()
from bolt.models import Shelter, Animal
from datetime import date

def populate():
    shelters = {
        'ResQ': {'contact_number': '+447586329174', 'address':'Glasgow Central'},
        'Mission Possible': {'contact_number': '+447236329174', 'address':'77 Kelvinhaugh Street'},
        'Dogs Trust': {'contact_number': '+44 3758642374', 'address':'Buchanan View'},
    }
    animals = [
        {'name':'Fido', 'kind':'DOG', 'description':'Happy Boy!', 'adoption_status':'ADOPTED', 'adoption_date':date.today()},
        {'name':'Snow', 'kind':'CAT', 'description':'Dont bother!', 'adoption_status':'ADOPTED', 'adoption_date':date.today()},
        {'name':'Fury', 'kind':'BIRD', 'description':'Dont feed!', 'adoption_status':'UNKNOWN', 'adoption_date':date.today()},
    ]

    
    for shelter_name, shelter_data in shelters.items():
        s = add_shelter(shelter_name, contact_number=shelter_data['contact_number'], address=shelter_data['address'])
        for animal in animals:
            add_animal(s, animal)
    
def add_animal(shelter, animal):
    a = Animal.objects.get_or_create(shelter=shelter, name=animal['name'])[0]
    a.kind = animal['kind']
    a.description = animal['description']
    a.adoption_status = animal['adoption_status']
    a.adoption_date = animal['adoption_date']
    a.save()

def add_shelter(name, contact_number, address):
    s = Shelter.objects.get_or_create(name=name, contact_number=contact_number, address=address)[0]
    s.save()
    return s

if __name__ == '__main__':
    print("Starting Bolt population script...")
    populate()