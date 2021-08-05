from django.contrib import admin
from bolt.models import Animal, Shelter

class ShelterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Animal)
admin.site.register(Shelter, ShelterAdmin)