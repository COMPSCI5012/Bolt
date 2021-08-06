from django.contrib import admin
from django.contrib.auth.models import User
from bolt.models import Animal, Shelter, UserProfile, Fqa

class ShelterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Animal)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(UserProfile)
admin.site.register(Fqa)
